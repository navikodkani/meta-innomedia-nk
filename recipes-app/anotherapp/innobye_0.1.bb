SUMMARY = "Bye world app test."
DESCRIPTION = "Try to build using a makefile via oe_runmake"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

# Keeps getting checksum error pulling from GitHub so nerf it... (doesn't seem to work?)
BB_STRICT_CHECKSUM = "0"

# If local folder in 'src'
# SRC_URI = "file://src"


# This pulls using git protocol but need to provide a source version
SRC_URI = "git://github.com/innomediahho/innobyehh01.git;branch=main"
# Some version?
SRCREV = "main"

# Where to keep downloaded source files (in tmp/work/...)
# S = "${WORKDIR}/src"

# Git pulled source ends up in a folder called 'git'
S = "${WORKDIR}/git"


# Cross-compile source (Can do makefiles...)
do_compile() {
  oe_runmake
}

# Plant into the embedded system rootfs /usr/bin image
do_install() {
  oe_runmake install DESTDIR=${D} BINDIR=${bindir}
}

python do_display_banner() {
    bb.plain("***********************************************");
    bb.plain("*                                             *");
    bb.plain("* Howard's innobye 1 GitHub bitbake-layer     *");
    bb.plain("*                                             *");
    bb.plain("***********************************************");
}

addtask display_banner before do_build
