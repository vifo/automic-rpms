#!/usr/bin/env bash
# ----------------------------------------------------------------------------
# This script will detect the actual version number of an Automic Automation
# Engine component given in a ZIP file (either complete image, or actual
# single component, e.g. "Operations Manager Agent Unix Linux").
#
# Usage: get_component_version_number.sh <zip_filepath> <component_name>
#
# Example: get_component_version_number.sh \
#              Automation.Engine_Agent_Unix_Linux_9_8_7+hf.7.build.386.zip \
#              ucxjlx6
#
# Please note, that the version number will me mangled, so it can be
# safely used in RPM version numbers, i.e.:
#
#   9.00A333-981            => 9.333.981
#   10.0.2+hf.2.build.717   => 10.0.2.2.717
#   10.0.2+build.624        => 10.0.2.1.624
#
# Component name must be either the original one, or one of the predefined
# aliases.
#
#   Original name       Alias
#   ucxjli3             agent_unix_linux_x86
#   ucxjlx6             agent_unix_linux_x64
#   ucxjli6             agent_unix_linux_ia64
#
# Original names can be found in the docs.
# ----------------------------------------------------------------------------
# DISCLAIMER
#
# Automic Software Inc. did neither develop, approve nor release any part of
# this software. I am not in any way affiliated with Automic Software Inc.,
# but merely a simple customer.
#
# Further, i am not responsible for any damage done by using this software or
# you getting fired because you blew up your data center. If you have any
# concerns about this software, it is YOUR responsibility to do further
# research, ask questions the smart way (http://goo.gl/Rims), patch and/or
# doing it manually.
#
# USE AT YOUR OWN RISK, YOU HAVE BEEN WARNED.
# ----------------------------------------------------------------------------

# TODO: getopts

# main action below
zip_filepath="$1"
component_name="$2"

if [ ! -f "$zip_filepath" ] || [ -z "$component_name" ]; then
    echo "Usage: $0 <zip_filepath> <component_name>" >&2
    exit 1
fi

# Map aliases to actual component name.
case "$component_name" in
    "agent_unix_linux_x86")
        component_name="ucxjli3"
        ;;
    "agent_unix_linux_x64")
        component_name="ucxjlx6"
        ;;
    "agent_unix_linux_ia64")
        component_name="ucxjli6"
        ;;
esac

zip_filename=$(basename "$zip_filepath")
zip_extract_dir=$(mktemp -d)
component_tar_filename="${component_name}.tar.gz"

# Unzip ZIP file in temporary directory and check, if we can find a .tar.gz
# matching component name in it. If yes, continue and extract .tar.gz also.
unzip -q -j "$zip_filepath" "*/${component_name}.tar.gz" -d "$zip_extract_dir"
cd "$zip_extract_dir"

if [ ! -f "$component_tar_filename" ]; then
    echo "ERROR: Unable to find ${component_tar_filename} in ZIP file ${zip_filename}. Stop" >&2
    exit 1
fi

tar -xzf "$component_tar_filename"
rm "$component_tar_filename"

# For versions <= 8, the versioning scheme is ^\d+\-\d+$ (e.g. "400-417"). For
# versions >= 9, the versioning scheme is '^(9|10)(\.\d+){1,}(\+build\.\d+)?$'
# (e.g. 10.0.2+build.123).

if strings bin/* | grep -q '^[89].00A$'; then

    major_version=$(strings bin/* | perl -ne 'do { print $1; exit } if m/^([89]).00A$/')
    minor_version=$(strings bin/* | pcregrep '^\d+\-\d+$' | uniq)
    if [ -n "$minor_version" ]; then

        # We have a version number formatted as YDD-DHH used in V8 and V9.
        # Y=last digit of current year number, DDD=current day of year,
        # HH=hotfix/build number on this day.
        minor_version=$(echo "$minor_version" | tr '-' '.')
    fi
else
    # Expect V10+ version number. Extract minor version number (including
    # hotfix number and build number) with some regex magic.
    major_version="10"
    minor_version=$(strings bin/* | perl -ne "
        if (m{
            ^10                             # 10 only
            ((?:\.\d+){1,})                 # minor version number
            (?:\+
                (?:hf\.(\d+)\.?)?
                (?:build\.(\d+))?
            )
        }x) {
            \$minor = substr \$1, 1;
            \$hf    = \$2 || "1";
            \$build = \$3 || "1";

            printf '%s.%s.%s', \$minor, \$hf, \$build;
            exit;
        }")
fi

# Bail out, if we cannot get the version number.
if [ -z "$minor_version" ]; then
    echo "ERROR: Unable to get version number of ${component_name}. Stop" >&2
    echo "ERROR: Component has been extracted to \"${zip_extract_dir}\"" >&2
    exit 1
fi

echo "$major_version.$minor_version"

# Cleanup.
rm -rf "$zip_extract_dir"
