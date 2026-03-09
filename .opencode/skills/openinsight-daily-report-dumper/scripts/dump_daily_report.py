#!/usr/bin/env python3
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Persist an OpenInsight daily report into daily_report/<YYYYMMDD-HHMM>/"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read a single JSON payload from stdin",
    )
    return parser.parse_args()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


def main() -> int:
    args = parse_args()
    if not args.stdin:
        print("--stdin is required", file=sys.stderr)
        return 2

    raw = sys.stdin.read()
    if not raw.strip():
        print("stdin payload is empty", file=sys.stderr)
        return 2

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"invalid JSON payload: {exc}", file=sys.stderr)
        return 2

    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M")
    output_dir = Path("daily_report") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    result_path = output_dir / "result.json"
    atomic_write(result_path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    mail_html = payload.get("mail_html")
    if isinstance(mail_html, str):
        atomic_write(output_dir / "mail.html", mail_html)

    trace = payload.get("trace")
    if trace is not None:
        atomic_write(
            output_dir / "trace.json",
            json.dumps(trace, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )

    metadata = {
        "daily_report_path": output_dir.as_posix(),
        "result_json": result_path.as_posix(),
        "mail_html": (output_dir / "mail.html").as_posix() if isinstance(mail_html, str) else None,
        "trace_json": (output_dir / "trace.json").as_posix() if trace is not None else None,
        "timestamp_minute": timestamp,
    }
    print(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
