# ----------------------------------------------------------------------------
# RPM spec file for the UC4 Operations Manager Utilities.
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

%include uc4-om-defines.inc

Summary:            UC4 Operations Manager Utilities
Prefix:             %{__base_install_prefix}/utility
Name:               %{__base_package_name}-utility
Version:            %{__package_utility_version_major}.%{__package_utility_version_minor}
Release:            %{__package_utility_version_release}%{?dist}
Source0:            %{__package_utility_source_filename}
AutoReqProv:        no
Requires:           java >= 1.6

%description
UC4 Operations Manager is an enterprise automation platform by UC4 Software
Inc. This package contains the UC4 Operations Manager Utilities for Linux
(UTILLX6).

%prep
%setup -T -c
%__extract_component %{SOURCE0} %{__package_utility_component_name}

%install
rm -rf %{buildroot}
%__copy_files_from_build_to_buildroot_prefix
%__expand_paths_in_ini_files %{prefix}/bin %{buildroot}%{prefix}/bin/*.ori.ini
%__convert_newlines_to_lf %{buildroot}%{prefix}/bin/*.ori.ini

%files
%defattr(-,root,root,-)
%{prefix}

%clean
rm -rf %{buildroot}
