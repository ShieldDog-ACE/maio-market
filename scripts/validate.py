#!/usr/bin/env python3
"""Validate plugins.json and models.json for maio-market.

No third-party dependencies. Run locally or in CI:

    python3 scripts/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,47}$")
MODEL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
REPO_RE = re.compile(r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load(name: str) -> dict:
    path = ROOT / name
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        err(f"{name}: missing")
        return {}
    except json.JSONDecodeError as exc:
        err(f"{name}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        err(f"{name}: top level must be an object")
        return {}
    if data.get("schema") != 1:
        err(f"{name}: schema must be 1")
    return data


def check_text(where: str, value, field: str, *, max_len: int) -> None:
    if not isinstance(value, str) or not value.strip():
        err(f"{where}: {field} must be a non-empty string")
        return
    if len(value) > max_len:
        err(f"{where}: {field} is longer than {max_len} characters")


def check_plugins() -> None:
    data = load("plugins.json")
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        err("plugins.json: plugins must be an array")
        return
    seen: set[str] = set()
    for i, item in enumerate(plugins):
        where = f"plugins.json[{i}]"
        if not isinstance(item, dict):
            err(f"{where}: must be an object")
            continue
        name = item.get("name")
        check_text(where, name, "name", max_len=48)
        if isinstance(name, str):
            if not NAME_RE.match(name):
                err(f"{where}: name must match {NAME_RE.pattern}")
            if name in seen:
                err(f"{where}: duplicate name {name!r}")
            seen.add(name)
        check_text(where, item.get("author"), "author", max_len=64)
        repo = item.get("repo")
        if not isinstance(repo, str) or not REPO_RE.match(repo):
            err(f"{where}: repo must look like https://github.com/<owner>/<repo>")
        check_text(where, item.get("description"), "description", max_len=280)
        if "branch" in item:
            check_text(where, item["branch"], "branch", max_len=64)
        tags = item.get("tags", [])
        if not isinstance(tags, list) or len(tags) > 8:
            err(f"{where}: tags must be an array of at most 8 strings")
        else:
            for tag in tags:
                check_text(where, tag, "tag", max_len=24)


def check_models() -> None:
    data = load("models.json")
    models = data.get("models")
    if not isinstance(models, list):
        err("models.json: models must be an array")
        return
    seen: set[str] = set()
    for i, item in enumerate(models):
        where = f"models.json[{i}]"
        if not isinstance(item, dict):
            err(f"{where}: must be an object")
            continue
        name = item.get("name")
        check_text(where, name, "name", max_len=64)
        if isinstance(name, str):
            if not MODEL_NAME_RE.match(name):
                err(f"{where}: name must match {MODEL_NAME_RE.pattern}")
            if name in seen:
                err(f"{where}: duplicate name {name!r}")
            seen.add(name)
        check_text(where, item.get("author"), "author", max_len=64)
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            err(f"{where}: url must be an https:// URL")
        check_text(where, item.get("description"), "description", max_len=280)
        for field in ("context", "size"):
            value = item.get(field, 0)
            if not isinstance(value, int) or value < 0:
                err(f"{where}: {field} must be a non-negative integer")
        sha = item.get("sha256", "")
        if sha and (not isinstance(sha, str) or not SHA_RE.match(sha)):
            err(f"{where}: sha256 must be empty or 64 lowercase hex characters")


def main() -> int:
    check_plugins()
    check_models()
    if errors:
        print("maio-market validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("maio-market: plugins.json and models.json are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
