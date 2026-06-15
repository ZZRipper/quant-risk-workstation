# Quant Risk Workstation

Multi-strategy portfolio risk dashboard prototype for stock-level alpha strategies.

## What This Project Contains

```text
quant-risk-workstation-project/
  frontend/
    index.html
    styles.css
    app.js
  data/
    portfolio.json
    strategies.json
    strategy_validation.json
    strategy_correlation.json
    factor_exposures.json
    macro_regime.json
    risk_proxies.json
    nav_series.json
    market.json
    market_news.json
    data_bundle.js
  scripts/
    build_dashboard_data.py
    fetch_market_data.py
    strategy_library.py
    risk_metrics.py
  docs/
    data_schema.md
    project_methodology.md
  reports/
    strategy_validation_report.md
```

## How To Open

Option 1: open directly:

```text
frontend/index.html
```

Option 2: serve locally from the project root:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/frontend/index.html
```

## How To Regenerate Data

From the project root:

```bash
python3 scripts/build_dashboard_data.py
```

This script writes all dashboard JSON files into `data/`.

To refresh the deployable static site folder after regenerating data:

```bash
python3 scripts/prepare_public.py
```

This copies `frontend/` and `data/` into `public/`, which is the folder used by static hosting platforms.

## Public Link Deployment

For a stable link that other people can open and that updates when you push changes, connect this project to a GitHub repository and deploy it with Netlify or Render.

### Netlify

This repo includes `netlify.toml`.

Netlify settings:

```text
Build command: python3 scripts/prepare_public.py
Publish directory: public
```

After connecting the GitHub repo, every push will publish the committed dashboard data and update the same public Netlify link. Regenerate Yahoo data locally before committing when you want to refresh the dashboard numbers.

## Automated Daily Data Refresh

The repo includes a GitHub Actions workflow:

```text
.github/workflows/update-dashboard-data.yml
```

It runs after the regular U.S. market close on weekdays and can also be started manually from GitHub:

```text
Actions -> Update dashboard data -> Run workflow
```

The workflow intentionally forces Yahoo Finance data:

```text
DASHBOARD_DATA_SOURCE=yahoo
```

If Yahoo is unavailable, the workflow fails and does not commit anything. This prevents synthetic fallback data from overwriting the public dashboard. When the workflow succeeds, it commits updated `data/`, `public/`, and `reports/` files; Netlify then redeploys the same public link.

### Render

This repo includes `render.yaml`.

Render will use:

```text
Build command: python3 scripts/prepare_public.py
Static publish path: public
```

After connecting the GitHub repo, every push will update the same public Render link using the committed `data/*.json` files.

## Optional: Yahoo Finance Data

The market loader now tries Yahoo Finance first through `yfinance`. If `yfinance` is not installed, the network is unavailable, or Yahoo returns incomplete data, the script automatically falls back to deterministic synthetic data.

Install optional data dependencies:

```bash
pip install -r requirements.txt
```

Then rerun:

```bash
python3 scripts/build_dashboard_data.py
```

Test Yahoo Finance connectivity:

```bash
python3 scripts/test_yahoo_finance.py
```

If the test prints recent AAPL rows, Yahoo Finance is connected. If it says `yfinance is not installed`, run the install command above in the same Python environment used by VSCode.

## Python Pipeline Files

- `scripts/fetch_market_data.py`: market data loader. Tries Yahoo Finance first, then falls back to deterministic synthetic data if unavailable.
- `scripts/strategy_library.py`: WorldQuant-style strategy definitions and stock-level strategy return logic.
- `scripts/risk_metrics.py`: Sharpe, drawdown, VaR/ES, beta, factor loading and risk-limit helpers.
- `scripts/macro_regime.py`: open-access macro regime overlay using FRED when available and ETF proxies as fallback.
- `scripts/strategy_validation.py`: research validation table and Markdown report generator.
- `scripts/strategy_correlation.py`: rolling realized strategy correlation matrix and high-correlation pair detector.
- `scripts/build_dashboard_data.py`: orchestrator that writes dashboard-ready JSON files.
- `scripts/test_yahoo_finance.py`: small connectivity test for Yahoo Finance.
- `scripts/backtest_engine.py`: generic strategy backtest engine. Converts strategy signals into weights, trades, transaction costs, PnL, NAV and metrics.

## Documentation

- `docs/data_schema.md`: JSON fields, formulas and risk-limit definitions.
- `docs/project_methodology.md`: project design, current assumptions, what is real vs placeholder, and implementation roadmap.

## Current Data Status

- Strategies are WorldQuant-style alpha candidates.
- Strategy holdings are stock-level large-cap USA tickers from a current S&P 100-style shared universe.
- Each strategy ranks the same S&P 100-style universe using data through t-1, selects the latest top 10 names, and holds them equal-weight for day t.
- Backtest window targets roughly five years of daily data when Yahoo history is available.
- `STR-01` through `STR-20` use the generic backtest engine end-to-end.
- Current formulas are explainable prototype alpha signals; they can be replaced with approved production formulas later without changing the dashboard pipeline.
- ETFs are used only as risk proxies and benchmark comparisons.
- Macro regime is a risk overlay, not a replacement for stock-level strategy signals.
- Market news is a placeholder feed for future API integration.
- `reports/strategy_validation_report.md` is the research evidence layer behind the dashboard.

## Next Step

Review the 20 prototype signal definitions, then replace or refine formulas where the assignment requires a stricter alpha definition.

## Future Data Sources

Potential upgrades after Yahoo Finance:

- `Polygon.io`: production-friendly equities, ETFs, trades, aggregates and news.
- `Tiingo`: equities, ETFs and news/sentiment-friendly data.
- `Alpha Vantage`: simple API for equities, FX, macro and news sentiment.
- `Nasdaq Data Link`: macro, alternatives and vendor datasets.
- `FRED`: rates, inflation, macro and economic indicators.
- `WRDS / CRSP / Compustat`: institutional-grade historical stock and fundamentals data.
- Internal SQL database: best long-term option once signals, positions and daily runs are standardized.
