#!/usr/bin/env python
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "pydicom",
# ]
# ///

"""organize_dicom

Scan one or more files or directories for DICOM files, read StudyInstanceUID
and SOPInstanceUID, and move files into an output directory organized by
StudyInstanceUID. Within each study directory, files are named SOP_UID.dcm.

Usage: organize-dicom [--out-dir OUT] [--dry-run] [paths...]
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from typing import Dict

import pydicom


def iter_files(paths: list[str]):
    """Yield file paths found under each path. Direct files yielded as-is;
    directories are walked recursively."""
    for path in paths:
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in files:
                    yield os.path.join(root, name)
        else:
            # if the path is a glob pattern or doesn't exist, try as-is
            if '*' in path or '?' in path:
                import glob

                for f in glob.glob(path):
                    if os.path.isfile(f):
                        yield f
            else:
                # nothing to yield
                continue


def read_uids(path: str):
    """Return (study_uid, sop_uid) or (None, None) if not a dicom or missing uids."""
    try:
        ds = pydicom.dcmread(path, stop_before_pixels=True, force=True)
    except Exception:
        return (None, None)

    study = ds.get("StudyInstanceUID")
    sop = ds.get("SOPInstanceUID")
    # Some files may store UIDs in file_meta; accept those too
    if study is None:
        study = getattr(ds, "StudyInstanceUID", None) or ds.file_meta.get("StudyInstanceUID")
    if sop is None:
        sop = getattr(ds, "SOPInstanceUID", None) or ds.file_meta.get("SOPInstanceUID")

    if study is None or sop is None:
        return (None, None)
    return (str(study), str(sop))


def make_safe_filename(name: str) -> str:
    # strip path-unfriendly characters
    return "".join(c for c in name if c.isalnum() or c in ("-", "_", "."))


def organize(paths: list[str], out_dir: str, dry_run: bool = False, verbose: bool = False):
    # Map study -> sop -> source file path
    index: Dict[str, Dict[str, str]] = {}

    for filepath in iter_files(paths):
        study, sop = read_uids(filepath)
        if not study or not sop:
            if verbose:
                print(f"Skipping (not DICOM or missing UIDs): {filepath}")
            continue
        if study not in index:
            index[study] = {}
        index[study][sop] = filepath

    if not index and verbose:
        print("No DICOM files found with StudyInstanceUID + SOPInstanceUID")

    # Prepare output
    out_dir = os.path.abspath(out_dir)
    if not dry_run:
        os.makedirs(out_dir, exist_ok=True)

    for study, sops in index.items():
        study_dirname = make_safe_filename(study)
        study_dir = os.path.join(out_dir, study_dirname)
        if not dry_run:
            os.makedirs(study_dir, exist_ok=True)
        for sop, src in sops.items():
            sop_safe = make_safe_filename(sop)
            dst_name = f"{sop_safe}.dcm"
            dst = os.path.join(study_dir, dst_name)
            # Skip if file is already in the right place
            src_abs = os.path.abspath(src)
            if src_abs == os.path.abspath(dst):
                if verbose:
                    print(f"Already organized: {src}")
                continue
            # if destination exists, append a numeric suffix before extension
            if os.path.exists(dst):
                base, ext = os.path.splitext(dst_name)
                suffix = 1
                while True:
                    candidate = f"{base}-{suffix}{ext}"
                    candidate_path = os.path.join(study_dir, candidate)
                    if not os.path.exists(candidate_path):
                        dst = candidate_path
                        break
                    suffix += 1
            if verbose or dry_run:
                print(f"{('DRY ' if dry_run else '')}Moving: {src} -> {dst}")
            if not dry_run:
                try:
                    shutil.move(src, dst)
                except Exception as exc:
                    print(f"Failed to move {src} -> {dst}: {exc}", file=sys.stderr)


def parse_args(argv: list[str]):
    p = argparse.ArgumentParser(description="Organize DICOM files into study-based directories")
    p.add_argument("paths", nargs="*", help="Files or directories to scan (defaults to current directory if omitted)")
    p.add_argument("--out-dir", default="dicom", help="Output base directory (default: ./dicom)")
    p.add_argument("--dry-run", action="store_true", help="Show what would be moved without moving")
    p.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = p.parse_args(argv)
    if not args.paths:
        args.paths = ["."]
    return args


def main(arguments):
    args = parse_args(arguments)
    organize(args.paths, args.out_dir, dry_run=args.dry_run, verbose=args.verbose)


def cli():
    import sys

    return main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(cli())
