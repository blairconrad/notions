#!/usr/bin/env python

"""\
Summarize DICOM files, printing very basic identifying information.
"""

from __future__ import print_function
import os
import sys
import argparse
import glob
import pydicom
import logging


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", default=".", help="path", nargs="?", type=str)
    parser.add_argument("--verbose", action="count", default=0)
    parser.add_argument(
        "--with",
        dest="with_attributes",
        metavar="WITH",
        default="",
        help="Add these (comma-separated) additional attributes",
    )
    parser.add_argument("--without", default="", help="Omit these (comma-separated) attributes")
    parser.add_argument("--exactly", default="", help="Show exactly these (comma-separated) attributes")

    args = parser.parse_args(arguments)

    logging.basicConfig(format="", level={1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, logging.WARN))

    def validate_attributes(attributes_string):
        attributes = attributes_string.split(",")
        for attribute in attributes:
            if not pydicom.datadict.tag_for_keyword(attribute):
                raise Exception("[" + attribute + "] is not a valid tag name")
        return attributes

    attributes = ["PatientID", "PatientName", "AccessionNumber"]
    if args.without:
        for attribute_to_skip in args.without.split(","):
            attributes.remove(attribute_to_skip)

    if args.with_attributes:
        attributes.extend(validate_attributes(args.with_attributes))

    if args.exactly:
        attributes = attributes.extend(validate_attributes(args.exactly))

    specific_tags = attributes + ["SOPClassUID"]
    if "filename" in specific_tags:
        specific_tags.remove("filename")

    results = set()

    def get_files_from_source(source):
        if os.path.isfile(source):
            yield source
        elif os.path.isdir(source):
            for (dirpath, dirnames, filenames) in os.walk(source):
                for filename in filenames:
                    yield os.path.join(dirpath, filename)
        else:
            for expanded_source in glob.glob(source):
                for file in get_files_from_source(expanded_source):
                    yield file

    for path in get_files_from_source(args.path):
        logging.debug("Checking %s", path)
        try:
            with pydicom.dcmread(path, force=True, specific_tags=specific_tags) as dataset:
                dataset.filename = path
                if dataset.get("SOPClassUID") is None:
                    logging.info("Skipping %s, as it appears not to be a DICOM file", path)
                    continue
                this_result = [str(dataset.get(attribute, "")) for attribute in attributes]
                results.add(tuple(this_result))
        except (Exception):
            logging.error("Skipping %s, as it could not be read", path, exc_info=True)

    results = sorted(results)
    print_table(attributes, results)


def print_table(headers, body_rows):
    def find_column_widths(headers, rows):
        widths = [len(header) for header in headers]
        for result in rows:
            for i in range(len(result)):
                widths[i] = max(widths[i], len(result[i]))
        return widths

    widths = find_column_widths(headers, body_rows)
    column_indices = range(len(headers))
    print("  ".join([headers[i] + (widths[i] - len(headers[i])) * " " for i in column_indices]))
    print("  ".join(["-" * widths[i] for i in column_indices]))

    for result in body_rows:
        print("  ".join([result[i] + (widths[i] - len(result[i])) * " " for i in column_indices]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
