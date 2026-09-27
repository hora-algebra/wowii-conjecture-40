#!/usr/bin/env python3
"""Verify and extract the inherited HOC files; never execute research code."""
from __future__ import annotations
import argparse
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile

ARCHIVE_SHA256 = "6253fc7c035978b39834344c19eeb76726180dc13062b9f393a6ea9c5bea0689"
ARCHIVE_BYTES = 52012
FILE_COUNT = 52
DECODED_BYTES = 551080
ROOTS = {"hoc-review-evidence", "hoc-independent-audit"}

def safe_name(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or "\\" in name or not p.parts or p.parts[0] not in ROOTS:
        raise ValueError(f"Unsafe archive path: {name!r}")
    return p

def extract(destination: Path) -> None:
    destination = destination.expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination must not exist: {destination}")
    base = Path(__file__).resolve().parent / "evidence"
    data = b"".join((base / f"inherited.tar.xz.part{i:02d}").read_bytes() for i in range(1, 8))
    if len(data) != ARCHIVE_BYTES or hashlib.sha256(data).hexdigest() != ARCHIVE_SHA256:
        raise ValueError("Inherited archive size/hash mismatch; do not use the evidence")
    destination.parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix=".hoc-unpack-", dir=destination.parent))
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:xz") as archive:
            members = archive.getmembers()
            if len(members) != FILE_COUNT or sum(m.size for m in members) != DECODED_BYTES:
                raise ValueError("Unexpected archive inventory or decoded size")
            seen: set[str] = set()
            for member in members:
                p = safe_name(member.name)
                if not member.isfile() or p.as_posix() in seen:
                    raise ValueError("Archive contains duplicate or non-regular entries")
                seen.add(p.as_posix())
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"Unreadable archive member: {p}")
                payload = stream.read()
                if len(payload) != member.size:
                    raise ValueError(f"Truncated archive member: {p}")
                target = scratch.joinpath(*p.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
        verified = 0
        for root in sorted(ROOTS):
            for row in (scratch / root / "SHA256SUMS.txt").read_text().splitlines():
                expected, relative = row.split(None, 1)
                relative = relative.removeprefix("*")
                p = safe_name(f"{root}/{relative}")
                target = scratch.joinpath(*p.parts)
                if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                    raise ValueError(f"Source manifest mismatch: {p}")
                verified += 1
        if verified != 50:
            raise ValueError(f"Unexpected source manifest entry count: {verified}")
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"Destination appeared during extraction: {destination}")
        os.rename(scratch, destination)
        print(f"Verified {FILE_COUNT} files, {verified} source checksums; extracted to {destination}")
        print("No research code executed. No OTR admission, certification or GO performed.")
    except BaseException:
        shutil.rmtree(scratch, ignore_errors=True)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New directory outside campaign worktrees")
    args = parser.parse_args()
    try:
        extract(args.output)
    except (OSError, ValueError, tarfile.TarError) as exc:
        parser.exit(1, f"HOC evidence extraction failed: {exc}\n")
