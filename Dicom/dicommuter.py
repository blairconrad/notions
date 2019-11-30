#!/usr/bin/env python
# -*- coding: utf8 -*-
"""dicommuter, a DICOM manuplator that uses pydicom

A dicommuter instance is a software stack machine
(Polish-notation interpreter) for viewing and manipulating DICOM
datasets. Inspired by PILDriver.

When called as a script, the command-line arguments are passed to
a dicommuter instance.  If there are no command-line arguments, the
module runs an interactive interpreter, each line of which is split into
space-separated tokens and passed to the execute method.

All operations consume their arguments off the stack (use `dup' to
keep copies around).  Use `verbose 1' to see the stack state displayed
before each operation.

"""

from __future__ import print_function

import pydicom


class Dicommuter(object):
    verbose = 0

    def do_verbose(self):
        """\
        usage: verbose <int:num>

        Set verbosity flag from top of stack.
        """
        self.verbose = int(self.do_pop())

    # The evaluation stack (internal only)

    stack = []  # Stack of pending operations

    def push(self, item):
        """Push an argument onto the evaluation stack."""
        self.stack.insert(0, item)

    def top(self):
        """Return the element at the top of the stack, without consuming it."""
        return self.stack[0]

    def pop_until_dataset(self):
        """Remove and return all elements until we hit a dataset"""
        values = []
        while not isinstance(self.top(), pydicom.Dataset):
            values.append(self.do_pop())
        return values

    # Stack-manipulation commands

    def do_clear(self):
        """\
        usage: clear

        Clear the stack.
        """
        self.stack = []

    def do_pop(self):
        """\
        usage: pop

        Discard the top element on the stack.
        """
        return self.stack.pop(0)

    # DICOM commands

    def do_open(self):
        """\
        usage: open <string:filename>

        Open the indicated file, read it, and push the dataset on the stack.
        """
        self.push(pydicom.dcmread(self.do_pop(), force=True))

    def do_show(self):
        """\
        usage: show [<string:keyword> …]

        Show the DICOM dataset at the top of the stack. Leaves the item
        on the stack.
        With supplied keywords, only shows those keywords (from the
        top-level elements).
        """
        keywords = self.pop_until_dataset()
        if keywords:
            for keyword in keywords:
                print(getattr(self.top(), keyword))
        else:
            print(self.top())

    def do_set(self):
        """\
        usage: set <string:keyword> <string:value> [<string:value>…] <dataset:ds>

        Set the value of an element. Any items at the top of the stack
        will be joined with spaces (ASCII 0x20) and used as the element's
        new value.
        """
        keyword = self.do_pop()
        value = " ".join(self.pop_until_dataset())
        dataset = self.top()
        setattr(dataset, keyword, value)

    def do_unset(self):
        """\
        usage: unset {<string:keyword>|<integer:key>} [{<string:keyword>|<integer:key>}…] <dataset:ds>

        Unset the value of an element or elements. Each item at the top of the stack
        will considered an element name to be unset.
        Examples:
            unset 0x00211011
            unset PatientState
        """
        element_names = self.pop_until_dataset()
        dataset = self.top()
        for name in element_names:
            if name and name[0].isdigit():
                key = int(name, 16)
                del dataset[key]
            else:
                del dataset[name]

    def do_save(self):
        """usage: save <dataset:ds>

        Save the dataset to its original file, leaving it on the stack.
        """
        dataset = self.top()
        dataset.save_as(dataset.filename)

    def do_help(self):
        """\
        usage: help [topic]

        Shows this help.
        """

        commands = sorted([m for m in dir(self) if m.startswith("do_")])
        for command in commands:
            doc = getattr(self, command).__doc__
            if doc:
                doc = doc.split("\n")[0]
                print(doc.strip().replace("usage: ", ""))

    # The interpreter loop

    def execute(self, list):
        """Interpret a list of Dicommuter commands."""
        list.reverse()
        while len(list) > 0:
            self.push(list[0])
            list = list[1:]
            if self.verbose:
                print("Stack: " + repr(self.stack))
            top = self.top()
            if not isinstance(top, str):
                continue
            funcname = "do_" + top
            if not hasattr(self, funcname):
                continue
            else:
                self.do_pop()
                func = getattr(self, funcname)
                func()


if __name__ == "__main__":
    import sys

    # If we see command-line arguments, interpret them as a stack state
    # and execute.  Otherwise go interactive.

    def format_item(item):
        if hasattr(item, "SOPInstanceUID"):
            return "<Dataset " + item.SOPInstanceUID + ">"
        else:
            return repr(item)

    commuter = Dicommuter()
    if len(sys.argv[1:]) > 0:
        commuter.execute(sys.argv[1:])
    else:
        prompt = Dicommuter.__name__.lower() + "> "
        print(Dicommuter.__name__, "says hello.")
        while True:
            try:
                if sys.version_info[0] >= 3:
                    line = input(prompt)
                else:
                    line = raw_input(prompt)
            except EOFError:
                print("\n" + prompt)
                break
            commuter.execute(line.split())
            print([format_item(item) for item in commuter.stack])
