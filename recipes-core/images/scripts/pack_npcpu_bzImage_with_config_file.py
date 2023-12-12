#!/usr/bin/env python3
####################################################################################
## INTEL CONFIDENTIAL
##
## Copyright 2017-2020 Intel Corporation.
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
#
## @file
#
# Internal build tool to combine npcpu_boot.cfg with
# an ARM bzImage kernel. Will append a header that is
# read by the BIOS to understand where the files are located.
#
##


import pdb
import re, sys, os, getopt, string, codecs, fnmatch, shutil, struct, binascii

def usage ():
    sys.exit("Syntax:  %s 'bzImage' 'npcpu_boot.cfg' \n%s\n" %
    (os.path.basename(sys.argv[0]),
    """\nFunction:\n
    This utility takes in a bzImage and boot config file (npcpu_boot.cfg).
    It then appends a C little endian structure to be read by the BIOS that
    has the information about the size and location of both the bzImage and
    the boot config file. The BIOS can use this information to read the kernel
    comand line and launch the kernel at runtime.
    Required Arguments (for creation):
    'bzImage'          Path to the NPCPU kernel image.
    'npcpu_boot.cfg'   Path to the NPCPU kernel boot config file (contains kernel command line).
    'outputFile'       The output filename
    Required Arguments (to separate config from kernel):
    'Config+Kernel'    The file that has the kernel and the config file combined already.
    """))


def main(argv) :
    ##### Read input arguments and options
    try:
        opts, args = getopt.getopt(argv[0:],"")
    except getopt.GetoptError:
        usage()

    separateConfig = False

    # If we just have 2 args, we are separating the kernel from config file.
    if len(args) == 2:
        separateConfig = True
    elif len(args) == 4:
        bzImageFile = args[1]
        configFile = args[2]
        outputFile = args[3]
    else:
        usage()

    # This is the struct format used.
    s = struct.Struct('< 8s L L L L')

    #If we are separating config from kernel
    if separateConfig:
        print("Separating config file form kernel using file: " + args[1])
        dir = os.path.dirname(os.path.realpath(__file__))
        inputFilePath = os.path.join(dir, os.path.normpath(args[1]))
        file = open(inputFilePath,'rb')
        bytes = file.read()

        #Get the structure from the begining of the opened file.
        structVal = s.unpack_from(bytes)

        #Make sure we have a valid header signature
        if structVal[0] == b'$KRNLCFG':
            print("Found Header Signature! " + structVal[0].decode("utf-8"))
            print("KernelImageSize: " + str(structVal[1]))
            print("KernelImageOffset: " + str(structVal[2]))
            print("BootConfigFileSize: " + str(structVal[3]))
            print("BootConfigFileOffset: " + str(structVal[4]))
            outputFileDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            try:
                #Write out the kernel config file
                #Seek file to Config File offset
                file.seek(structVal[4])
                configOutputPath = os.path.join(outputFileDir, 'npcpu_boot.cfg')
                configOutFile = open(configOutputPath, 'wb');
                configOutFile.write(file.read(structVal[3]))
                configOutFile.close()
                print("Wrote npcpu_boot.cfg out to file: "+configOutputPath)

                #Write out the kernel bzImage
                #Seek file to Kernel File offset
                file.seek(structVal[2])
                bzImageOutputPath = os.path.join(outputFileDir, 'npcpu_bzImage')
                bzImageOutFile = open(bzImageOutputPath, 'wb');
                bzImageOutFile.write(file.read(structVal[1]))
                bzImageOutFile.close()
                print("Wrote bzImage out to file: "+bzImageOutputPath)
            except:
                print("ERROR! There is trouble writing out the file, do you have write permissions?")
                return 1
        else:
            print("Could not find header signature! Are you sure this kernel has a npcpu_boot.cfg file attached?")
            return 1

    #Else we are combining config to kernel
    else:
        ## Get the absolute path for each input.
        dir = os.path.dirname(os.path.realpath(__file__))
        bzImagePath = os.path.join(dir, os.path.normpath(bzImageFile))
        configFilePath = os.path.join(dir, os.path.normpath(configFile))
        outputFilePath = os.path.join(dir, os.path.normpath(outputFile))

        print("Using %s for the NPCPU kernel." % bzImagePath)
        print("Using %s for the npcpu_boot.cfg file." % configFilePath)
        print("Output file path is %s." % configFilePath)

        # Get the file size of the 2 input files.
        bzImageSize = os.path.getsize(bzImagePath)
        configFileSize = os.path.getsize(configFilePath)

        # The kernel is always right after the header. The header MUST be 512 bytes.
        bzImageOffset = 512

        # Calculate the offset of the configfile.
        configFileOffset = bzImageOffset + bzImageSize

        # Create the header to wrap the ARM kernel and config file
        # The BIOS needs this in little endian format and exactly how
        # The structure is as listed below.

        ## The size of the structure must be 512 bytes.
        ## define NPCPU_HEADER_SIGNATURE SIGNATURE_64('$', 'K', 'R', 'N', 'L', 'C', 'F', 'G')
        ## Create the struct the BIOS is expecting.
        ## typedef struct{
        ##    UINT64 Signature;
        ##    UINT32 KernelImageSize;      //The size of the kernel image
        ##    UINT32 KernelImageOffset;    //The offset in bytes relative to the begining of the partition.
        ##    UINT32 BootConfigFileSize;   //The size of the boot config file.
        ##    UINT32 BootConfigFileOffset; //The offset in bytes relative to the begining of the partition.
        ##    UINT8 Reserved[488]; //To allign this structure to 512 bytes EMMC block size.
        ## } NpcpuKernelHeader;

        ## Should be little endian, need to pack the struct with the proper values.
        values = (b'$KRNLCFG', bzImageSize, bzImageOffset, configFileSize, configFileOffset)

        #Create the structure to write to file.
        packed_data = s.pack(*values)

        #Open bzImage file to write it out.
        bzImageFileH = open(bzImagePath,'rb')
        #Open boot config file to write it out.
        configFileH = open(configFilePath,'rb')

        # Read in the data from the files
        bzImageData = bzImageFileH.read()
        configFileData = configFileH.read()

        # Open the output file and write out
        # the data in the following order.
        # Header(512 B) + ARM bzImage + npcpu_boot.cfg
        destination = open(outputFilePath,'wb')
        destination.write(packed_data+bytearray(488)+bzImageData+configFileData)

        print("")
        print("Finished creating %s output file!" % outputFilePath)

    return 0
  
if __name__ == '__main__' :
  print ("\nIntel NPCPU kernel and config image creation tool.\n")
  sys.exit(main(sys.argv))
