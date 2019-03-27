#!/usr/bin/env python

"""\
Summarize DICOM files, printing very basic identifying information.
"""

from __future__ import print_function
import os
import sys
import argparse
import pydicom
import logging


def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--include-filenames", default=False, help="whether to output an entry for each filename", type=str
    )
    parser.add_argument("path", default=".", help="path", nargs="?", type=str)
    parser.add_argument("--verbose", action="count", default=0)

    args = parser.parse_args(arguments)

    logging.basicConfig(format="", level={1: logging.INFO, 2: logging.DEBUG}.get(args.verbose, logging.WARN))

    if args.include_filenames:
        format = "%-16s %-16s %-80s %s"
        headers = ("Patient ID", "Accession Number", "Patient Name", "filename")
    else:
        format = "%-16s %-16s %-80s"
        headers = ("Patient ID", "Accession Number", "Patient Name")

    results = set()

    for (dirpath, dirnames, filenames) in os.walk(args.path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            logging.debug("Checking %s", path)
            with pydicom.dcmread(path, force=True) as dataset:
                if dataset.get("SOPClassUID") is None:
                    logging.info("Skipping %s, as it appears not to be a DICOM file", path)
                    continue
                patient_id = dataset.PatientID
                patient_name = dataset.PatientName
                accession_number = dataset.AccessionNumber

                if args.include_filenames:
                    filename = os.path.relpath(os.path.join(dirpath, filename), ".")
                    results.add((patient_id, accession_number, str(patient_name), filename))
                else:
                    results.add((patient_id, accession_number, str(patient_name)))

    print(format % headers)
    for result in results:
        print(format % result)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
