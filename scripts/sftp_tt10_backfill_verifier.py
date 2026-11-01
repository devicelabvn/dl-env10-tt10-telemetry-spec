#!/usr/bin/env python3
"""
DeviceLab DL-ENV10: Circular 10/2021/TT-BTNMT .txt Telemetry Validator & sFTP Backfill Verifier
Product Datasheet: https://devicelab.vn/san-pham/dl-env10/
Technical Guide:   https://devicelab.vn/kien-thuc/quy-chuan-datalogger-dieu-39-thong-tu-10-2021-tt-btnmt/

Validates:
1. Filename pattern: [Tinh]_[CongTy]_[MaTram]_[YYYYMMDDHHMMSS].txt
2. UTF-8 without BOM encoding
3. 5 Tab-delimited (\t) columns per line: Parameter, Value, Unit, Timestamp (14 digits), Status (00/01/02)
"""

import os
import re
import sys
from datetime import datetime

FILENAME_REGEX = re.compile(r"^[A-Z0-9]+_[A-Z0-9]+_[A-Z0-9]+_(\d{14})\.txt$")
VALID_STATUS_CODES = {"00", "01", "02"}


def validate_tt10_file(filepath: str) -> tuple[bool, list[str]]:
    errors = []
    fname = os.path.basename(filepath)

    m = FILENAME_REGEX.match(fname)
    if not m:
        errors.append(
            f"Invalid filename '{fname}': expected [Tinh]_[CongTy]_[MaTram]_[YYYYMMDDHHMMSS].txt"
        )

    try:
        with open(filepath, "rb") as f:
            raw = f.read()
    except OSError as exc:
        return False, [f"Cannot read file: {exc}"]

    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append("File contains UTF-8 BOM (0xEF 0xBB 0xBF); use UTF-8 without BOM for Envisoft compatibility.")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return False, [f"Invalid UTF-8 encoding: {exc}"]

    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        errors.append("File is empty.")

    for idx, line in enumerate(lines, start=1):
        cols = line.split("\t")
        if len(cols) != 5:
            errors.append(
                f"Line {idx}: expected 5 Tab-separated columns, found {len(cols)} (check if spaces were used instead of '\\t')."
            )
            continue

        param, val_str, unit, ts_str, status = cols
        if not param.strip():
            errors.append(f"Line {idx}: empty parameter code.")
        try:
            float(val_str)
        except ValueError:
            errors.append(f"Line {idx}: invalid numeric value '{val_str}' for parameter '{param}'.")

        if not unit.strip():
            errors.append(f"Line {idx}: empty measurement unit for parameter '{param}'.")

        try:
            datetime.strptime(ts_str, "%Y%m%d%H%M%S")
        except ValueError:
            errors.append(f"Line {idx}: invalid timestamp '{ts_str}' (expected YYYYMMDDHHMMSS).")

        if status not in VALID_STATUS_CODES:
            errors.append(
                f"Line {idx}: invalid Circular 10 status code '{status}' (allowed: 00=Normal, 01=Calibration, 02=Sensor Error)."
            )

    return len(errors) == 0, errors


def main():
    sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "samples")
    targets = sys.argv[1:] if len(sys.argv) > 1 else [
        os.path.join(sample_dir, f) for f in sorted(os.listdir(sample_dir)) if f.endswith(".txt")
    ]

    all_passed = True
    for path in targets:
        ok, errs = validate_tt10_file(path)
        if ok:
            print(f"[PASS] {os.path.basename(path)}: Compliant with Article 39 Circular 10/2021/TT-BTNMT")
        else:
            all_passed = False
            print(f"[FAIL] {os.path.basename(path)}:")
            for e in errs:
                print(f"  - {e}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
