import argparse
import re
import sys
from pydicom import datadict


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tag",
        help="""
        An input DICOM tag as alphabetic key, 8-digit hexadecimal number, or decimal number.
        Examples: "PatientName", "00100010", or "1048592"
        """,
    )
    args = parser.parse_args()

    if re.match(r"^[\dA-Fa-f]{4},?[\dA-Fa-f]{4}$", args.tag):
        numeric_tag = int(args.tag.replace(",", ""), 16)
    elif re.match(r"^\d+$", args.tag):
        numeric_tag = int(args.tag, 10)
    else:
        numeric_tag = datadict.tag_for_keyword(args.tag)
    describe(numeric_tag)


def describe(numeric_tag):
    tag_info = datadict.get_entry(numeric_tag)

    group, elem = divmod(numeric_tag, 0x10000)
    print(f"name:      {tag_info[2]}")
    print(f"tag:       {group:04X},{elem:04X}")
    print(f"key:       {tag_info[4]}")
    print(f"VR:        {tag_info[0]}")
    print(f"VM:        {tag_info[1]}")
    if tag_info[3]:
        print(f"retired:   {tag_info[3]}")
    print(f"\npossibly helpful link: https://duckduckgo.com/?q=!ducky+site:dicom.innolitics.com+{numeric_tag:08X}")


if __name__ == "__main__":
    main(sys.argv[1:])
