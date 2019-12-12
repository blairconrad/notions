import os
import shutil
import tempfile

import pytest
import dicommuter

data_dir = None


def setup_module(module):
    base_dir = os.path.dirname(__file__)

    global data_dir
    data_dir = os.path.join(base_dir)


def test_help_should_list_topics(capsys):
    dicommuter.main(["help"])

    captured = capsys.readouterr()
    assert (
        """
help [topic]
open <string:filename>
save
set <string:keyword> <string:value>
show [<string:keyword> …]
unset <string:keyword>
""".lstrip()
        == captured.out
    )


def test_help_with_topic_should_describe_topic(capsys):
    dicommuter.main(["help", "open"])

    captured = capsys.readouterr()
    assert (
        """
open <string:filename>
  
  Open the indicated file, read it, and push the dataset on the stack.
  
""".lstrip()  # noqa
        == captured.out
    )


def test_open_file_should_open_file_that_exists():
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename])


def test_show_with_no_keys_should_show_whole_file(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "show"])

    captured = capsys.readouterr()
    assert captured.out.strip().startswith(
        "(0008, 0008) Image Type                          CS: ['DERIVED', 'SECONDARY', 'OTHER']\n"
    ) and captured.out.endswith("(fffc, fffc) Data Set Trailing Padding           OB: Array of 126 elements\n")


def test_show_with_one_key_should_show_element(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "show", "RegionOfResidence"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2152) Region of Residence                 LO: 'BROAD COVE'"


def test_show_with_multiple_keys_should_show_all_elements(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "show", "RegionOfResidence", "SOPInstanceUID"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "\n".join(
        [
            "(0010, 2152) Region of Residence                 LO: 'BROAD COVE'",
            "(0008, 0018) SOP Instance UID                    UI: 1.3.6.1.4.1.5962.1.1.4.1.1.20040826185059.5457",
        ]
    )


def test_show_with_numeric_key_should_show_element(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "show", "0x00101040"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 1040) Patient's Address                   LO: '10 REAL STREET'"


def test_set_missing_attribute_with_named_key_should_add_value(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "set", "EthnicGroup", "Human", "show", "EthnicGroup"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2160) Ethnic Group                        SH: 'Human'"


def test_set_existing_attribute_with_named_key_should_change_value(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "set", "RegionOfResidence", "Island of Nin", "show", "RegionOfResidence"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2152) Region of Residence                 LO: 'Island of Nin'"


def test_set_missing_attribute_with_numeric_key_should_add_value(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "set", "0x00102160", "Human", "show", "EthnicGroup"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2160) Ethnic Group                        SH: 'Human'"


def test_set_missing_attribute_with_unknown_named_key_should_error_out(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        dicommuter.main(["open", filename, "set", "PatientAstrologicalSign", "Aquarius", "show"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    captured = capsys.readouterr()
    assert captured.out.strip() == "Cannot set unknown key 'PatientAstrologicalSign'"


def test_set_missing_attribute_with_unknown_numeric_key_should_error_out(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        dicommuter.main(["open", filename, "set", "0x10112160", "Aquarius"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    captured = capsys.readouterr()
    assert captured.out.strip() == "Cannot set unknown key '0x10112160'"


def test_set_existing_attribute_with_numeric_key_should_change_value(capsys):
    filename = os.path.join(data_dir, "original.dcm")

    dicommuter.main(["open", filename, "set", "0x00102152", "Island of Nin", "show", "RegionOfResidence"])

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2152) Region of Residence                 LO: 'Island of Nin'"


def test_save_should_save_file(capsys):
    tempdir = tempfile.mkdtemp()
    new_dcm = os.path.join(tempdir, "original.dcm")

    shutil.copyfile(os.path.join(data_dir, "original.dcm"), new_dcm)

    dicommuter.main(["open", new_dcm, "set", "RegionOfResidence", "Island of Nin", "save"])
    dicommuter.main(["open", new_dcm, "show", "RegionOfResidence"])

    os.remove(new_dcm)
    os.removedirs(tempdir)

    captured = capsys.readouterr()
    assert captured.out.strip() == "(0010, 2152) Region of Residence                 LO: 'Island of Nin'"


def test_unset_should_remove_element(capsys):
    filename = os.path.join(data_dir, "original.dcm")
    dicommuter.main(["open", filename, "unset", "RegionOfResidence", "show"])

    captured = capsys.readouterr()
    assert "Region of Residence" not in captured.out
