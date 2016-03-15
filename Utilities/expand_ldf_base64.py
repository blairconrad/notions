#!/usr/bin/env python

import sys
import base64


def main(args):
    global state
    global multi_line_buffer
    global output_file

    in_filename = args[0]

    output_file = file(in_filename.replace('.ldf', '.expanded.ldf'), 'wb')

    state = None
    multi_line_buffer = []

    for line in file(in_filename):
        process_line(line)

    if multi_line_buffer:
        write(base64.b64decode(''.join(multi_line_buffer)), '\n')

    return 0


def write(*args):
    global output_file
    for arg in args:
        output_file.write(arg)


def process_line(line):
    global state
    global multi_line_buffer

    if state is None:
        # expecting an attribute
        if line.endswith(':: \n'):
            state = 'multi_line'
            multi_line_buffer = []

        write(line)

    elif state == 'multi_line':
        if line.startswith(' '):
            multi_line_buffer.append(line.strip())
        else:
            write(base64.b64decode(''.join(multi_line_buffer)), '\n')
            state = None
            process_line(line)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
