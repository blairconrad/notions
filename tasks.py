import sys
import os.path

from invoke import task


def get_root_dir():
    return os.path.dirname(__file__)


def add_sources_to_sys_path():
    base_dir = os.path.dirname(__file__)
    for path in [base_dir + "/Dicom"]:
        if path not in sys.path:
            sys.path = [path] + sys.path


@task(iterable=["like"])
def test(context, like, loop=False):
    import pytest

    add_sources_to_sys_path()

    args = ["tests", "--black", "--flake8", "--rootdir=" + get_root_dir()]
    if like:
        args += ["-k", " or ".join(like)]

    pytest.main(args)
