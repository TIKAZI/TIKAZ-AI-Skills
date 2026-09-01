from __future__ import annotations

import argparse
import json
import re


ON_PREFIX = re.compile(r"^\s*ON(?=$|\s|:|：)")


def route_request(text: str) -> dict[str, str]:
    match = ON_PREFIX.match(text)
    if not match:
        return {"mode": "economy", "task": text.strip()}
    task = text[match.end() :].lstrip(" \t\r\n:：")
    return {"mode": "onpremise", "task": task}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    print(json.dumps(route_request(args.text), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
