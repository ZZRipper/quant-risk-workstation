# Copilot / AI assistant instructions for Quant Risk Workstation

These notes are intended to make an AI coding assistant productive quickly in this repository.
Keep answers short and actionable: reference exact files and show concrete edits or commands.

1. Big picture (what the repo does)
- **Purpose**: prototype multi-strategy stock-level risk dashboard and backtest pipeline. Core output is frontend JSON under `data/` consumed by `frontend/index.html` (via `data/data_bundle.js`).
- **Major components**: `scripts/` (pipeline & analytics), `data/` (dashboard JSON), `frontend/` (simple static dashboard), `docs/` (data schema & methodology), `reports/` (validation reports).

2. Primary data flow and orchestration
- `scripts/build_dashboard_data.py` is the orchestrator: it calls `fetch_market_data.load_market_data()`, `strategy_library.build_strategy_objects()`, `backtest_engine.run_backtest()` and `risk_metrics` helpers, then writes `data/*.json` and `data/data_bundle.js`.
- Backtests are single-day rebalanced, long-only, and follow the timing convention in `scripts/backtest_engine.py`: strategies may only use history up to `day` (i.e., t-1 signals). When modifying strategy logic, follow that timing convention.

3. Key files to inspect or edit (examples)
- `scripts/build_dashboard_data.py`: pipeline constants (e.g. `BACKTEST_DAYS`, `TOP_N_HOLDINGS`, `INITIAL_CAPITAL`), JSON output names and `PROXY_LOADING_MAP` / `FACTOR_LIMITS` used by the UI.
- `scripts/fetch_market_data.py`: exposes `load_market_data(days, source)` and `LARGE_CAP_UNIVERSE`, `RISK_PROXIES`. It prefers `yfinance` and falls back to deterministic synthetic data—keep that fallback when adding external data sources.
- `scripts/strategy_library.py`: all strategy classes and `STRATEGY_SPECS` / `STRATEGY_CLASS_BY_INDEX`. New strategies should be added by appending a `StrategySpec` and the corresponding class in `STRATEGY_CLASS_BY_INDEX`.
- `scripts/backtest_engine.py`: `run_backtest(strategy, market_data, capital)` signature and `BacktestResult` dataclass. Respect `min_history` and `max_weight` attributes on `Strategy` subclasses.
- `frontend/app.js` and `frontend/index.html`: simple static UI—editing JSON shape requires parallel JSON + frontend updates.

4. Developer workflows & useful commands
- Regenerate dashboard JSON: `python3 scripts/build_dashboard_data.py` (writes into `data/`).
- Serve the frontend locally: `python3 -m http.server 8000` then open `http://localhost:8000/frontend/index.html`.
- Install optional dependencies (for Yahoo): `pip install -r requirements.txt`.
- Test Yahoo connectivity: `python3 scripts/test_yahoo_finance.py` (prints sample AAPL rows if connected).

5. Project-specific conventions & patterns to follow
- Strategy IDs: use `STR-01` .. `STR-20` format matching `STRATEGY_SPECS` ordering (see `strategy_library.py`).
- Signals use the t-1 convention: `strategy.signal(market_data, day)` must not use data at index `day` for computing the signal. Helper functions in `strategy_library.py` follow this convention.
- Holders/universe: all strategies currently share `LARGE_CAP_UNIVERSE`. To change per-strategy investable universes, update `holdings_for_strategy()` and `build_strategy_objects()`.
- Cost and turnover: BUY/SELL bps live as constants in `backtest_engine.py` and `build_dashboard_data.py` — change in one place only with care.

6. Integration points & external dependencies
- Optional: `yfinance` for market data; fallback is deterministic synthetic data. If adding Polygon/Tiingo, update `fetch_market_data.py` while preserving the current fallback behavior.
- `macro_regime.py` uses FRED when available; otherwise ETF proxies are used. Factor loadings and proxies are controlled by `PROXY_LOADING_MAP` in `build_dashboard_data.py`.

7. Common edits and examples (copy-paste ready)
- Add a new strategy:
  - Add a `Strategy` subclass in `scripts/strategy_library.py` implementing `signal(self, market_data, day)`.
  - Append a `StrategySpec` to `STRATEGY_SPECS` and add the class to `STRATEGY_CLASS_BY_INDEX` at the same index.
  - Ensure `min_history` and `max_weight` are set if different from defaults.

- Change output JSON shape:
  - Update `scripts/build_dashboard_data.py` write sections where `write_json(...)` is called, and then update `frontend/app.js` to match the new key names.

8. Safety notes for automated changes
- Do not remove the deterministic synthetic data fallback in `fetch_market_data.py` — tests and offline runs depend on it.
- Keep `data/` stable (names/keys) unless you also update `frontend/` and `reports/` consistently.

9. Where to look for further context
- `docs/data_schema.md`: canonical JSON field definitions and formulas used by the UI.
- `reports/strategy_validation_report.md`: research assumptions and what is intentionally prototype vs. realistic.

If anything here is unclear or you want the file to include more examples (unit-test snippets, CI steps, or commit rules), tell me which section to expand and I'll iterate.
