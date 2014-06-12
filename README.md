# automic-rpms

This repository contains RPM spec files and helpers for the [Automic Software Inc.][automic_com] [Automation Engine][automic_automation_engine] (formerly known as UC4 Operations Manager and rebranded in 2013).

## Disclaimer

Automic Software Inc. did neither develop, approve nor release any part of this software. I am not in any way affiliated with Automic Software Inc., but merely a simple customer.

Further, I am not responsible for any damage done by using this software or you getting fired because you blew up your data center. If you have any concerns about this software, it is **YOUR** responsibility to do further research, [ask questions the smart way][ask_questions_the_smart_way], patch and/or do it manually on your own.

**USE AT YOUR OWN RISK. YOU HAVE BEEN WARNED.**

## Motivation

Operations Manager/Automation Engine components have to be installed more or less manually from .tar.gz archives. Automic Software Inc. does not (yet) provide packaged downloads. This repository provides RPM spec files for the following components (not all are packaged yet, more to come):

* UC4 Operations Manager SAP Agent
* UC4 Operations Manager Service Manager
* UC4 Operations Manager UNIX Agent
* UC4 Operations Manager Utilities

## Usage

* Install [rpmbuild][rpmbuild_docs] (``yum install rpm-build``)
* Clone/download repo (``git clone https://github.com/vifo/automic-rpms``)
* Grab required ZIPs from [downloads.automic.com][automic_downloads] (prior [registration][automic_support] required). Ensure that version numbers match and/or adjust version numbers/ZIP filenames in spec files (``specs/uc4-om-defines.inc``). Copy grabbed ZIPs to ``~/rpmbuild/SOURCES``.
* Copy additional required files from ``sources/`` to ``~/rpmbuild/SOURCES``
* Run build with ``cd specs/ && rpmbuild -ba uc4-om-utility.spec``

## Limitations

* Currently, only V8 builds are supported.
* Batteries not included. Since Automic requires a registration prior to downloading ZIPs, the latter are not included. You have to [register first][automic_support] and [download][automic_downloads] them yourself.
* The spec files are targeted for [Red Hat Enterprise Linux (RHEL)][redhat_rhel] (and binary compatible). Other distributions *may* work, but have not been tested. Contributions, especially for [SUSE Linux Enterprise Server (SLES)][suse_sles], are of course welcome.
* The only architecture supported is `x86_64` (specified via ``ExclusiveArch`` in spec files). Trying to build for other architectures will (intentionally) fail. For now, it is unlikely at best that other architectures will be supported in the future. Again, contributions welcome.

## Links

* [Automic Software Inc.][automic_com]
* [Automic Software Inc. Downloads][automic_downloads]
* [Automic Software Inc. Support][automic_support]
* [Red Hat Enterprise Linux (RHEL)][redhat_rhel]
* [rpmbuild][rpmbuild_docs] man page
* [SUSE Linux Enterprise Server (SLES)][suse_sles]

[ask_questions_the_smart_way]: http://goo.gl/Rims
[automic_com]: http://www.automic.com/
[automic_downloads]: http://downloads.automic.com/
[automic_automation_engine]: http://automic.com/product
[automic_support]: https://automationpassion.com/
[rpmbuild_docs]: http://www.rpm.org/max-rpm-snapshot/rpmbuild.8.html
[suse_sles]: https://www.suse.com/products/server
[redhat_rhel]: http://www.redhat.com/products/enterprise-linux
