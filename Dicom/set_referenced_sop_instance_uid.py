#!/usr/bin/env python

import sys
import glob
import pydicom


def main(args):
    new_uid = args.pop(0)
    file_glob = args.pop(0)

    for filename in glob.glob(file_glob):
        set_sop_instance_uid(filename, new_uid)


def set_sop_instance_uid(filename, new_uid):
    ds = pydicom.dcmread(filename)
    set_sop_instance_uid_for_data_set(ds, new_uid)
    ds.save_as(filename)


def set_sop_instance_uid_for_data_set(ds, new_uid):
    for data_element in ds:
        if data_element.VR == 'SQ':
            for item in data_element.value:
                set_sop_instance_uid_for_data_set(item, new_uid)
        else:
            if data_element.name == 'Referenced SOP Instance UID':
                data_element.value = new_uid


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
