#!/usr/bin/env python

"""\
Inflate a dicom file whose transfer syntax is Deflated Explicit VR Little Endian
(1.2.840.10008.1.2.1.99). Writes to out.dcm.
"""

import sys
import argparse
import zlib

CURRENT_POSITION = 1


def read_tag(infile):
    group = read_int(infile, 2)
    element = read_int(infile, 2)
    return group * 0x10000 + element


def read_int(infile, length):
    int_text = infile.read(length)

    result = 0
    for i in range(length - 1, -1, -1):
        result *= 0x100
        result += int_text[i]

    return result


def skip(infile, length):
    infile.seek(length, CURRENT_POSITION)  # skip the VR


def read_vr_and_length(infile):
    vr = infile.read(2)
    if vr in [b"OB", b"OW", b"OF", b"SQ", b"UT", b"UN"]:
        infile.read(2)
        length = read_int(infile, 4)
    else:
        length = read_int(infile, 2)
    return (vr, length)

def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("infile", type=argparse.FileType("rb"))

    args = parser.parse_args(arguments)

    infile = args.infile

    infile.seek(128)  # skip the preamble
    dcm_tag = infile.read(4)
    if dcm_tag != b"DICM":
        print("Not a dicom file")
        return

    file_meta_information_group_length_tag = read_tag(infile)
    if file_meta_information_group_length_tag != 0x0002_0000:
        print("First tag is", file_meta_information_group_length_tag, "not File Meta Information Group Length")
        return

    (vr, file_meta_information_group_length_length) = read_vr_and_length(infile)
    file_meta_information_group_length = read_int(infile, file_meta_information_group_length_length)

    start_of_data_offset = infile.tell() + file_meta_information_group_length

    while True:
        transfer_syntax_uid_tag = read_tag(infile)
        if transfer_syntax_uid_tag == 0x0002_0010:
            break

        # print("Tag", hex(transfer_syntax_uid_tag), "is not Transfer Syntax UID at " + str(infile.tell()))
        (vr, length) = read_vr_and_length(infile)
        infile.read(length)

    (vr, transfer_syntax_uid_length) = read_vr_and_length(infile)
    transfer_syntax_uid = infile.read(transfer_syntax_uid_length)

    if transfer_syntax_uid != b"1.2.840.10008.1.2.1.99":
        print("Transfer syntax UID is", transfer_syntax_uid, "not Deflated Explicit VR Little Endian")
        return

    infile.seek(start_of_data_offset)
    compressed_rest = infile.read()
    decompressed_rest = zlib.decompress(compressed_rest, -zlib.MAX_WBITS)

    header = (
        b"\x00" * 128
        + b"DICM"
        + b"\x02\x00\x00\x00"
        + b"UL"
        + b"\x04\x00\x1b\x00\x00\x00\x02\x00\x10\x00UI\x13\x001.2.840.10008.1.2.1"
    )
    with open("out.dcm", "wb") as outfile:
        outfile.write(header)
        outfile.write(decompressed_rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
