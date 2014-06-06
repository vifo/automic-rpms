# ----------------------------------------------------------------------------
# RPM spec file for the UC4 Operations Manager UNIX Agent for Linux.
#
# Refer to https://github.com/vifo/automic-rpms for details/docs.
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
# do it manually on your own.
#
# USE AT YOUR OWN RISK. YOU HAVE BEEN WARNED.
# ----------------------------------------------------------------------------
# FIXME: After removal of package, the following dir structure is left over:
#
#   /opt/uc4/
#   /opt/uc4/agents
#
# /opt/uc4 must not exist at all after removal. Any ideas?
# ----------------------------------------------------------------------------

%include uc4-om-defines.inc

Summary:            UC4 Operations Manager UNIX Agent for Linux
Prefix:             %{__base_install_prefix}/agents/unix
Name:               %{__base_package_name}-agent-unix
Version:            %{__package_agent_unix_version_major}.%{__package_agent_unix_version_minor}
Release:            %{__package_agent_unix_version_release}%{?dist}
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires(postun):   initscripts
Source0:            %{__package_agent_unix_source_filename}
Source1:            %{name}.init.d.sh

%description
UC4 Operations Manager is an enterprise automation platform by UC4 Software
Inc. This package contains the UC4 Operations Manager UNIX Agent for Linux
(UCXJLX6).

%prep
%setup -T -c
%__extract_component %{SOURCE0} %{__package_agent_unix_component_name}

%install
rm -rf %{buildroot}
%__copy_files_from_build_to_buildroot_prefix
%__expand_paths_in_ini_files %{prefix}/bin %{buildroot}%{prefix}/bin/*.ori.ini

# Install initscript and replace variables in init script.
mkdir -p %{buildroot}%{_initrddir}
install -m755 -oroot -groot %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
perl -i -p \
    -e "s!\%\{prefix\}!%{prefix}!;" \
    -e "s!\%\{name\}!%{name}!" \
    %{buildroot}%{_initrddir}/%{name}

pushd %{buildroot}%{prefix}/bin
cp ucxjxxx.ori.ini UCXJLX6.ori.ini
cp ucxjxxx.ori.ini UCXJLX6M.ori.ini
rm ucxjxxx.ori.ini
popd

%__convert_newlines_to_lf %{buildroot}%{prefix}/bin/*.ori.ini

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

%clean
rm -rf %{buildroot}
