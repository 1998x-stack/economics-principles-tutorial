#!/usr/bin/env python3
"""Build the offline course catalog without third-party dependencies."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    data = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise ValueError("chapters must be a nonempty list")
    if data.get("chapterCount") != len(chapters):
        raise ValueError("chapterCount does not match chapters")
    for chapter in chapters:
        num = chapter.get("num")
        if not isinstance(num, str) or len(num) != 2 or not num.isdigit():
            raise ValueError("invalid chapter number")
        filename = num + ".html"
        if chapter.get("file") != filename or not (ROOT / filename).is_file():
            raise ValueError("invalid or missing chapter file: " + filename)
    return ("/* Generated from courses.json; run python3 scripts/build_course_data.py. */\n"
            "window.COURSE_CATALOG = " +
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "courses-data.js"
    expected = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            parser.error("courses-data.js is stale; regenerate it")
    else:
        target.write_text(expected, encoding="utf-8")


if __name__ == "__main__":
    main()
