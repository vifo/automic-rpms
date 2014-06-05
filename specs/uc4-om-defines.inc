# ----------------------------------------------------------------------------
# Macros tend to be a bit slashy :) Pay attention to correct escaping
# and line continuation, if changing macros. Forgetting a line continuation
# (especially at the end of a comment) can cause REAL headache.
#
# \\    => maps to \ in shell script
# \     => macro line continuation (needed at end of line)
# ----------------------------------------------------------------------------

# Base installation directory. Nothing (besides init scripts) will be installed
# outside this directory.
%define __base_install_prefix                           /opt/uc4

# Base package name all package names are prefixed with.
%define __base_package_name                             uc4-om

# ----------------------------------------------------------------------------
# Defines for each package built go below, each prefixed with
# "__package_whatever_".
#
# Each package will be built from a single ZIP file containing the
# appropriate component (i.e. a build of "uc4-om-agent-unix" can be
# configured via "__package_agent_unix_*" defines, and we need the ZIP file
# defined in "__package_agent_unix_source_filename").
#
# You can override this behavior, if using an image ZIP which contains all
# components in a single ZIP file. Point "__package_image_source_filename"
# to the appropriate ZIP.
#
# In either case, please ensure that version numbers are adjusted as
# appropriate.
# ----------------------------------------------------------------------------
#%define __package_image_source_filename                Operations.Manager_Image_8_9_14-05-28-1.zip

%define __package_agent_unix_version_major              8
%define __package_agent_unix_version_minor              407.791
%define __package_agent_unix_version_release            1
%define __package_agent_unix_component_name             ucxjlx6
%define __package_agent_unix_source_filename            Operations.Manager_Agent_Unix_Linux_8_9_0+build.2.zip

%define __package_agent_sap_version_major               8
%define __package_agent_sap_version_minor               408.092
%define __package_agent_sap_version_release             1
%define __package_agent_sap_source_filename             Operations.Manager_Agent_SAP_8_9_0+build.15.zip
%define __package_agent_sap_component_name              ucxjr3x

%define __package_utility_version_major                 8
%define __package_utility_version_minor                 408.092
%define __package_utility_version_release               1
%define __package_utility_source_filename               Operations.Manager_Utility_Linux_8_9_0+build.15.zip
%define __package_utility_component_name                utillx6

%define __package_service_manager_version_major         8
%define __package_service_manager_version_minor         227.061
%define __package_service_manager_version_release       1
%define __package_service_manager_source_filename       UC4.Operations.Manager_ServiceManager_8.00A_6_0.zip
%define __package_service_manager_component_name        ucsmgrlx6

# Macros. Skip them till "END_OF_MACROS". Do not miss any important settings
# below "END_OF_MACROS".
%define __copy_files_from_build_to_buildroot_prefix() \
    # * create BUILDROOT/PREFIX \
    # * copy BUILD/* => BUILDROOT/PREFIX \
    # * fix file permissions (not ownership) in BUILDROOT/PREFIX \
    mkdir -p %{buildroot}%{prefix}; \
    cp --preserve=mode,timestamps -R * %{buildroot}%{prefix}; \
    %__fix_file_permissions %{buildroot}%{prefix} \

%define __extract_component() \
    # Extract tar.gz with component from ZIP file. \
    # Remove .tar.gz afterwards. \
    unzip -j -q "%1" "*/%2.tar.gz"; \
    tar -xzf "%2.tar.gz"; \
    rm "%2.tar.gz"; \

%define __convert_newlines_to_lf() \
    perl -i -pe 's/\\r$//' %**; \

%define __fix_file_permissions() \
    # Attempt to set sensible default file permissions based on file \
    # extension. \
    chmod -R u=rwX,g=rX,o=rX "%1"; \
    find "%1" -type f -a \\( \\\
        -name '*.sh' \\\
        -name '*.so' \\\
    \\) -print0 | xargs -0 --no-run-if-empty chmod 755; \
    find "%1" -type f -a \\( \\\
           -name '*.ini' \\\
        -o -name '*.msl' \\\
        -o -name '*.smd' \\\
        -o -name '*.jar' \\\
    \\) -print0 | xargs -0 --no-run-if-empty chmod 644; \

%define __expand_paths_in_ini_files() \
    # Expand paths in INI files. \
    perl -i -p -e " \\\
        BEGIN { \\$basedir = '%1'; shift @ARGV; }; \\\
        s{ \\\
            ^\\s*(output|docu_path|logging|file|deffile|cmdfile|helplib)\\s*\\=\\s*(.*?)\\s*\\$ \\\
        }{ \\\
            \\$key = \\$1; \\\
            \\$value = \\$2; \\\
            @result = split /\\//, \\$basedir; \\\
            @path = split /\\//, \\$value; \\\
            while (defined(\\$path_elem = shift @path)) { \\\
                unless (\\$path_elem =~ m/^\\./) { \\\
                    push @result, \\$path_elem; \\\
                    push @result, @path; \\\
                    last; \\\
                } \\\
                if (\\$path_elem eq '..') { \\\
                    pop @result; \\\
                } \\\
            }; \\\
            sprintf \\"%s = %s\\n\\", \\$key, join('/', @result); \\\
        }xei;" \\\
    %**; \

# END_OF_MACROS

# Tags common to all packages go here.
#
# TODO: Overriding a value below is a PITA, since it has to be copied into
# every spec file (and removed here). Better way?
ExclusiveArch:      x86_64
Group:              Applications/System
Packager:           Victor Foitzik <vifo@cpan.org>
License:            Proprietary
URL:                http://www.automic.com/
