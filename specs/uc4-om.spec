# ----------------------------------------------------------------------------
# RPM spec file for the UC4 Operations Manager.
#
# Please note, that "UC4 Software Inc." has been rebranded in 2013 to "Automic
# Software Inc.", while "Operations Manager" has been renamed to "Automation
# Engine". This has been reflected by two separate .spec files, depending on
# version, i.e.:
#
#     uc4-om.spec                   # for <= V8
#     automic-ae.spec               # for >= V9
#
# ----------------------------------------------------------------------------
# DISCLAIMER
#
# Automic Software Inc. did neither develop, approve nor release any part of
# this software. I am not in any way affiliated with Automic Software Inc.,
# but merely a simple customer.
#
# Further, I am not responsible for any damage done by using this software or
# you getting fired because you blew up your data center. If you have any
# concerns about this software, it is YOUR responsibility to do further
# research, ask questions the smart way (http://goo.gl/Rims), patch and/or
# doing it manually.
#
# USE AT YOUR OWN RISK. YOU HAVE BEEN WARNED.
# ----------------------------------------------------------------------------

%define __base_install_prefix                       /opt/uc4
%define __base_package_name                         uc4-om

%define __package_agent_linux_version_major         8
%define __package_agent_linux_version_minor         407.791
%define __package_agent_linux_version_release       1
%define __package_agent_linux_source_filename       Operations.Manager_Agent_Unix_Linux_8_9_0+build.2.zip

# Component names. Should not be changed normally.
%define __uc4_agent_linux_component_name            ucxjlx6

# Section for UC4 Operations Manager Linux Agent
Prefix:             %{__base_install_prefix}/agents/unix
Name:               %{__base_package_name}-agent-linux
Version:            %{__package_agent_linux_version_major}.%{__package_agent_linux_version_minor}
Release:            %{__package_agent_linux_version_release}%{?dist}
ExclusiveArch:      x86_64
Group:              Applications/System
Summary:            UC4 Operations Manager Agent for Linux
License:            Proprietary
URL:                http://www.automic.com/
Packager:           Victor Foitzik <vifo@cpan.org>
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
Source0:            %{__package_agent_linux_source_filename}
Source1:            %{name}.init.d.sh

%description
This package contains the UC4 Operations Manager Agent for Linux (UCXJLX6).

%prep
%setup -T -c

# Extract tar.gz with component from ZIP file. Remove .tar.gz afterwards.
unzip -j -q %{SOURCE0} */%{__uc4_agent_linux_component_name}.tar.gz
tar -xzf %{__uc4_agent_linux_component_name}.tar.gz
rm %{__uc4_agent_linux_component_name}.tar.gz

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{prefix}
cp -a * %{buildroot}%{prefix}

chmod -R u=rwX,g=rX,o=rX    %{buildroot}%{prefix}
chmod -R 644                %{buildroot}%{prefix}/bin/*.ini
chmod -R 644                %{buildroot}%{prefix}/bin/*.msl

# Install initscript and replace variables in init script.
mkdir -p %{buildroot}%{_initrddir}
install -m755 -oroot -groot %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
perl -i -p \
    -e "s!\%\{prefix\}!%{prefix}!;" \
    -e "s!\%\{name\}!%{name}!" \
    %{buildroot}%{_initrddir}/%{name}

# Adjust INI files and convert all relative paths to absolute ones.
pushd %{buildroot}%{prefix}/bin
perl -i -p \
    -e "s!(\=\s*)\./\$!\${1}%{prefix}/bin/!;" \
    -e "s!(\=\s*)\../(temp|out)/!\${1}%{prefix}/\${2}/!;" \
    -e "s!(helplib\s*\=\s*)(.*)!\${1}%{prefix}/bin/\${2}!;" \
    ucxjxxx.ori.ini

cp ucxjxxx.ori.ini UCXJLX6.ori.ini
cp ucxjxxx.ori.ini UCXJLX6M.ori.ini
rm ucxjxxx.ori.ini
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_initrddir}/%{name}
%{prefix}

%post
# TODO: Check, if we're upgrading or performing a new installation. On
# upgrades, keep previous run state of service. On new installations, turn it
# off by default.

# Add proper /etc/rc*.d links for init script.
/sbin/chkconfig --add %{name}

%preun
# Run this section on removal only ("$1" -eq "0"), but not on upgrades.
if [ "$1" -eq "0" ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
# Run this section on upgrades only ("$1" -gt "0").
if [ "$1" -gt "0" ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi

%changelog
