SUMMARY = "My custom innomedia linux image."
IMAGE_LINGUAS = " "
LICENSE = "MIT"

# Hack to force our image name to be preferred so that build will complete
PREFERRED_PROVIDER_virtual/core-image-gateway:remove = "core-image-gateway-${INTEL_SOC}-arm-${INTEL_DISTRO}"
PREFERRED_PROVIDER_virtual/core-image-gateway = "custom-image"

# add packagegroup-intelce-arm-common and packagegroup-docsis to IMAGE_INSTALL
require common-core-image-arm.inc

# Include modules in rootfs
IMAGE_INSTALL += " \
packagegroup-puma7  \
packagegroup-gw     \
"

python do_display_banner() {
    bb.plain("***********************************************");
    bb.plain("*                                             *");
    bb.plain("* Howard's recipe created by bitbake-layers   *");
    bb.plain("*                                             *");
    bb.plain("***********************************************");
}

addtask display_banner before do_build

# put our custom myapp
IMAGE_INSTALL += " innohello "
IMAGE_INSTALL += " innobye "
