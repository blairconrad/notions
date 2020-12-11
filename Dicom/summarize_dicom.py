#!/usr/bin/env python

"""\
Summarize DICOM files, printing very basic identifying information.
"""

import os
import sys
import argparse
import glob
import pydicom
import logging


def main(arguments):

    epilog = """examples:
  %(prog)s directory_full_of_dicom_files
  %(prog)s --with StudyInstanceUID --with filename directory_full_of_dicom_files
  %(prog)s --with StudyInstanceUID --without AccessionNumber directory_full_of_dicom_files"""

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog
    )
    parser.add_argument("path", default=".", help="path", nargs="*", type=str)
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Output additional progress and state information."
        " May be specified more than once to increase the amount of information output.",
    )
    parser.add_argument(
        "--with",
        dest="with_attributes",
        action="append",
        metavar="ATTRIBUTE",
        help="Add this additional DICOM attribute (use Pascal Case, e.g. StudyInstanceUID). "
        " May be specified more than once to add multiple attributes."
        " The special attribute 'filename' may also be used.",
    )
    parser.add_argument(
        "--without",
        metavar="ATTRIBUTE",
        action="append",
        help="Omit this attribute from the report. May be specified more than once to omit multiple attributes.",
    )
    parser.add_argument(
        "--exactly",
        metavar="ATTRIBUTE",
        action="append",
        help="Show exactly this attribute. May be specified more than once to show multiple attributes.",
    )

    args = parser.parse_args(arguments)

    logging.basicConfig(format="", level={1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, logging.WARN))

    def validate_attributes(attributes):
        for attribute in attributes:
            if attribute != "filename" and not pydicom.datadict.tag_for_keyword(attribute):
                raise Exception("[" + attribute + "] is not a valid tag name")
        return attributes

    attributes = ["PatientID", "PatientName", "AccessionNumber"]
    if args.without:
        for attribute_to_skip in args.without:
            attributes.remove(attribute_to_skip)

    if args.with_attributes:
        attributes.extend(validate_attributes(args.with_attributes))

    if args.exactly:
        attributes = validate_attributes(args.exactly)

    specific_tags = attributes + ["SOPClassUID"]
    if "filename" in specific_tags:
        specific_tags.remove("filename")

    results = set()

    def get_files_from_source(sources):
        for source in sources:
            if os.path.isfile(source):
                yield source
            elif os.path.isdir(source):
                for (dirpath, dirnames, filenames) in os.walk(source):
                    for filename in filenames:
                        yield os.path.join(dirpath, filename)
            else:
                for file in get_files_from_source(glob.glob(source)):
                    yield file

    for path in get_files_from_source(args.path):
        logging.debug("Checking %s", path)
        try:
            with pydicom.dcmread(path, force=True, specific_tags=specific_tags) as dataset:
                dataset.filename = path
                if dataset.get("SOPClassUID") is None:
                    logging.info("Skipping %s, as it appears not to be a DICOM file", path)
                    continue
                this_result = [get_attribute(dataset, attribute) for attribute in attributes]
                results.add(tuple(this_result))
        except (Exception):
            logging.error("Skipping %s, as it could not be read", path, exc_info=True)

    results = sorted(results)
    print_table(attributes, results)


def get_attribute(dataset, attribute_name):
    value = attribute_name in dataset and dataset.get(attribute_name) or dataset.file_meta.get(attribute_name, "")
    return str(value)


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
