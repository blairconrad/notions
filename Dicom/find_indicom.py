#!/usr/bin/env python

"""\
Find dicom files whose attributes meet a certain criterion
"""

from __future__ import print_function
import os
import sys
import argparse
import pydicom
import logging


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("matcher", type=str, help="What to match on. Of the form AttributeName=Value.")
    parser.add_argument("path", default=".", help="path", nargs="?", type=str)
    parser.add_argument("--verbose", action="count", default=0)

    args = parser.parse_args(arguments)

    logging.basicConfig(level={1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, logging.WARNING))

    (attribute, value) = args.matcher.split("=")

    for (dirpath, dirnames, filenames) in os.walk(args.path):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            try:
                with pydicom.dcmread(filename) as dataset:
                    if dataset.get(attribute) == value:
                        print(os.path.relpath(filename))
            except pydicom.errors.InvalidDicomError:
                logging.info("Skipping %s, as it appears not to be a DICOM file", filename)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
