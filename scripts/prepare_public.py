#!/usr/bin/env python3
"""Prepare the static dashboard folder for deployment."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
DATA_DIR = ROOT / "data"
PUBLIC_DIR = ROOT / "public"
PUBLIC_DATA_DIR = PUBLIC_DIR / "data"
DOCS_DIR = ROOT / "docs"
DOCS_DATA_DIR = DOCS_DIR / "data"


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_index(dst: Path) -> None:
    content = (FRONTEND_DIR / "index.html").read_text(encoding="utf-8")
    content = content.replace("../data/data_bundle.js", "./data/data_bundle.js")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8")


def prepare_site(target_dir: Path, data_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    copy_index(target_dir / "index.html")
    for name in ("app.js", "styles.css"):
        copy_file(FRONTEND_DIR / name, target_dir / name)

    for path in DATA_DIR.glob("*.json"):
        copy_file(path, data_dir / path.name)

    bundle = DATA_DIR / "data_bundle.js"
    if bundle.exists():
        copy_file(bundle, data_dir / bundle.name)


def main() -> None:
    prepare_site(PUBLIC_DIR, PUBLIC_DATA_DIR)
    prepare_site(DOCS_DIR, DOCS_DATA_DIR)
    print(f"Prepared static site in {PUBLIC_DIR}")
    print(f"Prepared GitHub Pages site in {DOCS_DIR}")


if __name__ == "__main__":
    main()
