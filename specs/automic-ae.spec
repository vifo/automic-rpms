# ----------------------------------------------------------------------------
# RPM spec file for the Automic Automation Engine.
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

%define __package_name              "uc4-operations-manager"
%define __package_release           1
%define __uc4_version_major         8
%define __uc4_version_minor         8
%define __uc4_version_build         8

Name:           %{__package_name}
Version:        %{__uc4_version_major}
Release:        %{__package_release}%{?dist}
Group:          Applications/System
Summary:        Dummy test package
License:        Proprietary
URL:            http://www.automic.com/
Packager:       Victor Foitzik <vifo@cpan.org>

%description
lorem ipsum

%prep
%setup -T -c
