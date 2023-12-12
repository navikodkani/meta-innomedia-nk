####################################################################################
## INTEL CONFIDENTIAL
##
## Copyright 2015-2020 Intel Corporation.
##
## DISTRIBUTABLE AS SAMPLE SOURCE SOFTWARE
##
## This Distributable As Sample Source Software is subject to the terms and
## conditions of the Intel Software License Agreement for the Intel(R) Cable
## and GW Software Development Kit
##
## This software and the related documents are Intel copyrighted materials, and
## your use of them is governed by the express license under which they were
## provided to you ("License"). Unless the License provides otherwise, you may
## not use, modify, copy, publish, distribute, disclose or transmit this
## software or the related documents without Intel's prior written permission.
##
## This software and the related documents are provided as is, with no express
## or implied warranties, other than those that are expressly stated in the License.
####################################################################################

inherit sstrip create_intel_report
inherit kernel_version_to_current_symlink
inherit intel_sdk

# Base this image on core-image-minimal
include recipes-core/images/core-image-minimal.bb

IMAGE_INSTALL += " \
	 packagegroup-intelce-arm-common \
	 ${@bb.utils.contains('DISTRO_FEATURES', 'docsis', 'packagegroup-docsis', '', d)} \
	 "

PROVIDES = "virtual/core-image-gateway"
SCRIPT_DIR:="${THISDIR}/scripts"

# remake do_rootfs every time
do_rootfs[nostamp] = "1"

# allow to use setcap utility in pkg_postins_${PN} tasks
do_rootfs[depends] += "libcap-native:do_populate_sysroot"
