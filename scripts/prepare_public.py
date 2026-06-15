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


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for name in ("index.html", "app.js", "styles.css"):
        copy_file(FRONTEND_DIR / name, PUBLIC_DIR / name)

    for path in DATA_DIR.glob("*.json"):
        copy_file(path, PUBLIC_DATA_DIR / path.name)

    bundle = DATA_DIR / "data_bundle.js"
    if bundle.exists():
        copy_file(bundle, PUBLIC_DATA_DIR / bundle.name)

    print(f"Prepared static site in {PUBLIC_DIR}")


if __name__ == "__main__":
    main()
