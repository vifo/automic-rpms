# automic-rpms

This repository contains RPM spec files and helpers for the Automic Software Inc. Automation Engine (formerly known as UC4 Operations Manager).

## Disclaimer

Automic Software Inc. did neither develop, approve nor release any part of this software. I am not in any way affiliated with Automic Software Inc., but merely a simple customer.

Further, I am not responsible for any damage done by using this software or you getting fired because you blew up your data center. If you have any concerns about this software, it is **YOUR** responsibility to do further research, [ask questions the smart way][ask_questions_the_smart_way], patch and/or doing it manually.

**USE AT YOUR OWN RISK. YOU HAVE BEEN WARNED.**

## Motivation

Operations Manager/Automation Engine components have to be installed more or less manually from .tar.gz archives. Automic Software Inc. does not (yet) provide packaged downloads. This repository provides RPM spec files for the following components (not all are packaged yet, more to come):

* UC4 Operations Manager SAP Agent for Linux
* UC4 Operations Manager UNIX Agent for Linux
* UC4 Operations Manager utilities

## Usage

* Install [rpmbuild][rpmbuild_docs] (``yum install rpm-build``)
* Clone/download repo (``git clone https://github.com/vifo/automic-rpms``)
* Grab required ZIPs from [Automic][automic_downloads] (registration required). Ensure that version numbers match and/or adjust spec files (especially ``specs/uc4-om-defines.inc`` and ``specs/automic-ae-defines.inc`` respectively)
* Copy downloaded ZIPs to ``~/rpmbuild/SOURCES``
* Copy required files from ``sources/`` to ``~/rpmbuild/SOURCES``
* Run (for example) ``rpmbuild -ba specs/uc4-om-utility.spec``

## Limitations

* Batteries not included. Since Automic requires a registration prior to downloading ZIPs, the latter are not included. You have to download them yourself.
* Currently, only V8/V9 builds are supported.
* The spec files are targeted for Red Hat Enterprise Linux. Other distributions *may* work, but have not been tested.
* The only architecture supported is `x86_64` (specified via `ExclusiveArch` in spec files). Trying to build for other architectures will (intentionally) fail. For now, it is unlikely at best that other architectures will be supported in the future. Contributions are of course welcome.

[ask_questions_the_smart_way]: http://goo.gl/Rims
[automic_com]: http://www.automic.com/
[automic_downloads]: https://automationpassion.com/
[rpmbuild_docs]: http://www.rpm.org/max-rpm-snapshot/rpmbuild.8.html
