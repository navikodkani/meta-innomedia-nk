SUMMARY = "My hello world app test."
DESCRIPTION = "Bah blah blah"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# Useful info about how to do this but not yet helpful:
# https://stackoverflow.com/questions/37705995/how-to-compile-a-basic-c-file-in-yocto

# Keeps getting checksum error pulling from GitHub so nerf it... (doesn't seem to work?)
BB_STRICT_CHECKSUM = "0"



# Where to find the source files (can be local, Git, etc.)
# SRC_URI = "git://server.com/PATH/TO/ti-linux-kernel.git;protocol=https"
## SRC_URI = "git://github.com/innomediahho/innohellohh01.git;protocol=https"

# If local folder in 'src'
# SRC_URI = "file://src"

# This works but downloads from GitHub like a tar... Need to figure out how to make it work via git protocol
#SRC_URI = "http://github.com/innomediahho/innohellohh01/archive/refs/heads/main.zip;protocol=http"
#SRC_URI[sha256sum] = "dd9989a02cbc291e69d6f1d1f87528668c9f95279312acf45f666cb4905ec4f5"

# This pulls using git protocol but need to provide a source version
SRC_URI = "git://github.com/innomediahho/innohellohh01.git;branch=main"
# Some version?
SRCREV = "main"



# Where to keep downloaded source files (in tmp/work/...)
# S = "${WORKDIR}/src"

# Against the main.zip file the folder created by GitHub is 'innohellohh01-main'
#S = "${WORKDIR}/innohellohh01-main"

# Git pulled source ends up in a folder called 'git'
S = "${WORKDIR}/git"


# Pass arguments to linker (required)
TARGET_CC_ARCH += "${LDFLAGS}"

# Cross-compile source (Can do makefiles...)
do_compile() {
  ${CC} -o innohello innohello.c
}

# Plant into the embedded system rootfs /usr/bin image
do_install() {
  install -d ${D}${bindir}
  install -m 0755 innohello ${D}${bindir}
}

python do_display_banner() {
    bb.plain("***********************************************");
    bb.plain("*                                             *");
    bb.plain("* Howard's innohello 2 GitHub bitbake-layer   *");
    bb.plain("*                                             *");
    bb.plain("***********************************************");
}

addtask display_banner before do_build
