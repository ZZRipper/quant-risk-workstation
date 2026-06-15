#!/usr/bin/env python3
"""Quick Yahoo Finance connectivity test."""

from __future__ import annotations


def main() -> None:
    try:
        import yfinance as yf
    except ImportError:
        print("yfinance is not installed.")
        print("Run: pip install -r requirements.txt")
        raise SystemExit(1)

    data = yf.download("AAPL", period="5d", interval="1d", auto_adjust=True, progress=False)
    if data.empty:
        print("Yahoo Finance responded, but returned no AAPL data.")
        raise SystemExit(1)

    print("Yahoo Finance connection OK.")
    print(data.tail())


if __name__ == "__main__":
    main()
