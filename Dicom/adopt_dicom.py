#!/usr/bin/env python

"""'Adopt' one or more DICOM files into an existing patient or study
"""

from __future__ import print_function
import os
import sys
import argparse
import pydicom


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("adopter", help="File that represents the family to adopt the targets into.")
    parser.add_argument("level", help="The level at which to adopt the object.", choices=["PATIENT", "STUDY"])
    parser.add_argument("adoptee", nargs="+", help="DICOM file to enroll into the 'family'. Will be edited in place.")

    args = parser.parse_args(arguments)

    attributes_to_update = ["PatientID", "PatientName"]
    if args.level == "STUDY":
        attributes_to_update += ["StudyID", "StudyInstanceUID", "AccessionNumber"]

    with pydicom.dcmread(args.adopter, force=True) as adopter:
        for adoptee in args.adoptee:
            with pydicom.dcmread(adoptee, force=True) as ds:
                for attribute_to_update in attributes_to_update:
                    setattr(ds, attribute_to_update, getattr(adopter, attribute_to_update))
                ds.save_as(adoptee)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
