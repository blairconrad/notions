notions-dicom-tools
===================

Overview

This directory bundles several standalone DICOM helper scripts into a single installable package for use with uv. Scripts live in the notions_dicom package and are exposed as console tools when the package is installed.

Key facts
- Package name: notions-dicom-tools
- Python requirement: >=3.14
- Third-party dependency: pydicom (auto-installed by uv)
- Console tools installed: adopt-dicom, summarize-dicom, set-sop-uid, find-indicom, describe-tag, inflate-dicom, dicommuter

Install (editable, for development)

  cd D:\Dev\notions\Dicom
  uv tool uninstall notions-dicom-tools   # remove old installs if needed
  uv tool install --editable .

Run installed tools

  adopt-dicom ADOPTER PATIENT file.dcm
  summarize-dicom path/to/dicom/dir
  set-sop-uid NEW_UID "*.dcm"
  find-indicom PatientID=12345
  describe-tag PatientName
  inflate-dicom compressed.dcm
  dicommuter            # interactive

Run without installing (uv will create an env for the script):

  uv run D:\Dev\notions\Dicom\notions_dicom\summarize_dicom.py -- <args>

Implementation notes

- Each script exposes a cli() function that forwards sys.argv[1:] to the script's main() function.
- Per-script project directories and egg-info were removed to avoid conflicts with editable installs; the single Dicom-level pyproject.toml is authoritative.
- If an executable is missing or misbehaves, uninstall the package, remove any leftover *.egg-info directories in this folder, then reinstall (see Install steps).

If you want a different layout (one project per script or a proper package module layout), say so and a different structure can be prepared.