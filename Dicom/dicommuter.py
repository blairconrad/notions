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

The results of many operations consume arguments from an internal stack
of objects (usually 1 deep), which consists of the result of previous
commands. For example the command

    open <filename>

will read the file <filename>, produce a DICOM dataset object and push it
on the stack. Then

     set PatientName SURNAME^GIVEN

will set the PatientName attribute in the top object, leaving it on the stack.
"""

from __future__ import print_function

import pydicom


class Dicommuter(object):
    # The evaluation stack (internal only)
    stack = []  # Stack of pending operations

    def push(self, item):
        """Push an argument onto the evaluation stack."""
        self.stack.insert(0, item)

    def top(self):
        """Return the element at the top of the stack, without consuming it."""
        return self.stack[0]

    def get_command(self, command_name):
        "Get the command with the given name, or return None"
        return getattr(self, "do_" + command_name, None)

    def pop_until_command(self, tokens):
        """Remove and return all tokens until we find a command"""
        values = []

        while tokens and not self.get_command(tokens[0]):
            values.append(tokens.pop(0))
        return values

    # def pop_until_dataset(self):
    #     """Remove and return all elements until we hit a dataset"""
    #     values = []
    #     while not isinstance(self.top(), pydicom.Dataset):
    #         values.append(self.do_pop())
    #     return values

    # # Stack-manipulation commands

    # def do_clear(self):
    #     """\
    #     usage: clear

    #     Clear the stack.
    #     """
    #     self.stack = []

    # def do_pop(self):
    #     """\
    #     usage: pop

    #     Discard the top element on the stack.
    #     """
    #     return self.stack.pop(0)

    # DICOM commands

    def do_open(self, tokens):
        """\
        usage: open <string:filename>

        Open the indicated file, read it, and push the dataset on the stack.
        """
        filename = tokens.pop(0)
        self.push(pydicom.dcmread(filename, force=True))
        return tokens

    def do_show(self, tokens):
        """\
        usage: show [<string:keyword> …]

        Show the DICOM dataset at the top of the stack. Leaves the item
        on the stack.
        With supplied keywords, only shows those keywords (from the
        top-level elements).
        """
        keywords = self.pop_until_command(tokens)
        if keywords:
            for keyword in keywords:
                print(getattr(self.top(), keyword))
        else:
            print(self.top())
        return tokens

    def do_set(self, tokens):
        """\
        usage: set <string:keyword> <string:value>

        Set the value of an element in the top dataset of the stack.
        """
        keyword = tokens.pop(0)
        value = tokens.pop(0)
        dataset = self.top()
        setattr(dataset, keyword, value)
        return tokens

    def do_unset(self, tokens):
        """\
        usage: unset <string:keyword>

        Unset the value of an element
        Examples:
            unset PatientState
        """
        keyword = tokens.pop(0)
        dataset = self.top()

        del dataset[keyword]

        return tokens

    def do_save(self, tokens):
        """usage: save

        Save the dataset to its original file, leaving it on the stack.
        """
        dataset = self.top()
        dataset.save_as(dataset.filename)

        return tokens

    def do_help(self, tokens):
        """\
        usage: help [topic]

        Shows help.
        """

        if tokens:
            command_to_show = tokens.pop(0)
            function = self.get_command(command_to_show)
            if not function:
                raise Exception(f"Invalid command '{command_to_show }'.")
            doc = [l.strip() for l in function.__doc__.split("\n")]
            doc[0] = doc[0].replace("usage: ", "")
            print("\n  ".join(doc))

        else:
            commands = sorted([m for m in dir(self) if m.startswith("do_")])
            for command in commands:
                doc = getattr(self, command).__doc__
                if doc:
                    doc = doc.split("\n")[0]
                    print(doc.strip().replace("usage: ", ""))
        return tokens

    # The interpreter loop

    def execute(self, tokens):
        """Interpret a list of Dicommuter commands."""
        while tokens:
            command = tokens.pop(0)
            function_name = "do_" + command
            function = getattr(self, function_name, None)
            if not function:
                raise Exception(f"Invalid command '{command}'.")
            tokens = function(tokens)


def main(args):

    # If we see command-line arguments, interpret them as a script
    # and execute.  Otherwise go interactive.

    def format_item(item):
        if hasattr(item, "SOPInstanceUID"):
            return "<Dataset " + item.SOPInstanceUID + ">"
        else:
            return repr(item)

    commuter = Dicommuter()
    if args:
        commuter.execute(args)
    else:
        prompt = Dicommuter.__name__.lower() + "> "
        print(Dicommuter.__name__, "says hello.")
        while True:
            try:
                line = input(prompt)
            except EOFError:
                print("\n" + prompt)
                break
            commuter.execute(line.split())


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
