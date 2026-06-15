# Quant Risk Workstation Project Methodology

## 1. Project Goal

The goal of this project is to build a multi-strategy portfolio risk workstation for researching, backtesting and monitoring stock-level alpha strategies.

The dashboard is not intended to be a simple performance display. It should help a portfolio manager or risk manager answer:

- Which strategies are contributing or hurting?
- Which strategies are breaching risk limits?
- Are strategies becoming too correlated?
- Are factor exposures concentrated?
- Are transaction costs dragging performance?
- Should we rebalance, reduce, pause, hedge or increase a strategy?

## 2. Key Scope Decisions

### Strategies Are Stock-Level Alpha Strategies

The main strategies are based on underlying U.S. stocks.

Examples:

- Momentum on large-cap stocks
- Short-term reversal on large-cap stocks
- Volume-price confirmation
- Low-volatility stock selection
- Range breakout / volatility behavior

### ETFs Are Risk Proxies, Not Strategies

ETFs are used for comparison and factor interpretation only.

Examples:

| ETF | Use |
|---|---|
| SPY | Market beta proxy |
| QQQ | Growth / technology proxy |
| IWM | Size / small-cap proxy |
| TLT | Rates duration proxy |
| HYG | Credit spread proxy |
| LQD | Investment-grade credit proxy |
| GLD | Gold / real asset proxy |
| DBC | Commodity proxy |
| UUP | U.S. dollar proxy |

The dashboard should not describe ETF proxies as actual strategy holdings unless a future strategy explicitly trades ETFs.

## 3. Current Architecture

```text
Yahoo Finance / synthetic fallback
        ↓
fetch_market_data.py
        ↓
strategy_library.py
        ↓
backtest_engine.py
        ↓
risk_metrics.py
        ↓
build_dashboard_data.py
        ↓
data/*.json
        ↓
frontend dashboard
```

## 4. Project Folder Structure

```text
quant-risk-workstation-project/
  frontend/
    index.html
    styles.css
    app.js
  data/
    portfolio.json
    strategies.json
    factor_exposures.json
    risk_proxies.json
    nav_series.json
    market.json
    market_news.json
    data_bundle.js
  scripts/
    backtest_engine.py
    build_dashboard_data.py
    fetch_market_data.py
    risk_metrics.py
    strategy_library.py
    test_yahoo_finance.py
  docs/
    data_schema.md
    project_methodology.md
```

## 5. Data Source

The first real market data source is Yahoo Finance through `yfinance`.

The loader tries Yahoo first. If Yahoo fails or `yfinance` is unavailable, it falls back to deterministic synthetic data so the dashboard still runs.

```text
source="auto"
  → try Yahoo Finance
  → if unavailable, use synthetic data
```

The Market tab shows whether the current data source is `Yahoo` or `Synthetic`.

## 6. Strategy Workflow

Every strategy should eventually follow the same workflow:

```text
idea
  ↓
signal
  ↓
target weights
  ↓
trades / turnover
  ↓
transaction cost
  ↓
PnL
  ↓
NAV
  ↓
risk and performance metrics
  ↓
dashboard output
```

## 7. Meaning Of Core Terms

### Signal

The strategy's view on which stocks are more attractive.

Example:

```text
Short-term reversal signal = - past 5-day return
```

If a stock fell more over the past five days, the signal becomes higher.

### Weights

There are two different weight layers:

```text
Portfolio-level strategy allocation
  = how the $1,000,000 portfolio is split across strategies

Stock-level allocation inside each strategy
  = which stocks each strategy holds and how much each stock receives
```

Current stock-level rule inside each strategy:

- long-only
- all strategies rank the same S&P 100-style large-cap universe
- signal uses information through t-1
- select top 10 names
- equal weight the selected names
- hold those weights for day t
- calculate day t PnL from day t returns

This is intentionally simple for the first version. It can later be replaced by:

- rank weighting
- volatility-adjusted weighting
- sector-neutral weighting
- beta-neutral weighting
- optimizer-based allocation

### Turnover

How much the portfolio changes from one rebalance to the next.

Higher turnover usually means higher cost drag.

### Transaction Cost

Current assumption:

```text
Buy cost = 5 bps
Sell cost = 5 bps
Round trip = 10 bps
```

### PnL

Daily profit and loss:

```text
PnL = portfolio price return - transaction cost
```

### NAV

Net asset value:

```text
NAV_today = NAV_yesterday + PnL_today
```

### Metrics

Examples:

- Sharpe ratio
- Drawdown
- VaR
- Expected Shortfall
- Turnover
- Cost drag
- Factor beta
- Strategy correlation

## 8. Backtest Engine

The generic backtest engine is located in:

```text
scripts/backtest_engine.py
```

It handles:

- ranking the shared S&P 100-style large-cap universe by signal score
- selecting the top-N names
- assigning equal stock weights inside each strategy
- applying max single-stock weight caps
- calculating turnover
- applying transaction costs
- calculating daily PnL
- calculating NAV
- calculating Sharpe and drawdown

The goal is that every future strategy only needs to provide a signal function. The engine handles the rest.

### No-Lookahead Timing Convention

The current engine uses a close-to-close daily convention:

```text
signal at day t uses only data through t-1
top 10 equal-weight holdings are set for day t
PnL is earned on day t return
```

Each strategy also has a minimum history requirement. Before enough history is available, the engine stays in cash and records zero return/cost for that strategy.

This avoids direct lookahead bias from using same-day returns, prices or volume in the signal. It does not solve survivorship bias from using today's S&P 100-style universe; that requires a historical universe database such as CRSP/Compustat, WRDS, or another point-in-time constituent source.

### Strategy Correlation Timing

Strategy correlation is a risk-monitoring overlay, not a trading signal.

The dashboard uses rolling realized correlation:

```text
rolling 63 completed trading days of strategy returns
```

It is labeled with the window and as-of date in the dashboard. In a live workflow, the matrix should be computed from returns through the latest completed market close before it is used for allocation or risk decisions.

## 9. Current Strategy Implementation Status

| Strategy | Status |
|---|---|
| STR-01 WQ Alpha 001 - Short-Term Reversal | Full backtest engine enabled |
| STR-02 WQ Alpha 004 - Rank Momentum | Full backtest engine enabled |
| STR-03 WQ Alpha 006 - Volume Price Divergence | Full backtest engine enabled |
| STR-04 WQ Alpha 012 - Open-Close Pressure | Full backtest engine enabled |
| STR-05 WQ Alpha 021 - Trend Stability | Full backtest engine enabled |
| STR-06 to STR-20 | Full backtest engine enabled |

Important: all 20 strategies now run through the same backtest engine. Their current signals are prototype research definitions, not final production formulas.

## 10. Why Long-Only First?

The first version uses long-only strategies because it is easier to explain and monitor.

Long-only avoids extra assumptions such as:

- borrow cost
- short availability
- margin
- short rebate
- leverage limits
- gross exposure limits

Later versions can support:

- long-short market neutral
- beta neutral
- dollar neutral
- sector neutral
- 130/30

## 11. Factor Loading Methodology

Factor loading is represented as beta.

Conceptually:

```text
strategy_return = alpha + beta_factor * factor_return + residual
```

Current factor categories:

- Market beta
- Size beta
- Value beta
- Momentum beta
- Rates beta
- Credit beta
- Volatility beta
- USD beta
- Commodity beta

Factor betas are estimated from strategy or portfolio returns against factor proxy returns.

## 12. Macro Regime Overlay

The macro regime layer is a risk overlay, not a replacement for stock-level alpha signals.

It helps answer:

- Is the current environment risk-on or defensive?
- Are growth and inflation pressures rising or falling?
- Which strategy sleeves should be preferred, reduced or monitored?
- Does the portfolio have factor exposure that conflicts with the macro regime?

The first version tries open-access FRED data first:

- Industrial production
- Nonfarm payrolls
- Unemployment rate
- CPI
- 10Y breakeven inflation
- 10Y Treasury yield
- Baa credit spread
- VIX

If FRED is unavailable, it falls back to Yahoo ETF/factor proxies already used in the dashboard.

The regime is classified into four quadrants:

| Regime | Interpretation |
|---|---|
| Rising growth + rising inflation | Inflationary expansion |
| Rising growth + falling inflation | Risk-on / goldilocks |
| Falling growth + rising inflation | Stagflation risk |
| Falling growth + falling inflation | Defensive slowdown |

The dashboard uses this layer to provide strategy sleeve guidance and macro risk warnings.

## 13. Risk Limits

Risk limits are designed to be easy to explain.

Examples:

| Control | Warning | Breach |
|---|---:|---:|
| Strategy drawdown | <= -8% | <= -12% |
| Rolling Sharpe | < 0.25 | < -0.50 |
| Strategy correlation | > 0.65 | > 0.80 |
| Market beta | > 0.30 | > 0.45 |
| Macro beta | > 0.20 | > 0.35 |
| Cost drag | > 10 bps/month | > 20 bps/month |

The exact limits can be revised after real backtesting results are available.

## 14. What Is Real Now Vs Placeholder

### Implemented Now

- Dashboard layout
- JSON-driven frontend
- Yahoo Finance loader
- synthetic fallback
- generic backtest engine
- transaction cost model
- STR-01 short-term reversal signal
- STR-02 rank momentum signal
- STR-03 to STR-20 prototype alpha signals
- macro regime overlay using FRED or ETF proxy fallback
- portfolio-level JSON output
- factor beta framework
- risk proxy layer

### Still Placeholder

- exact production alpha formulas, if a stricter source formula is required later
- market news API
- optimized allocation
- true live positions
- real risk manager recommendation engine
- production data storage

## 15. Recommended Next Steps

### Step 1: Review Prototype Signal Definitions

Each strategy now has a signal function in `scripts/strategy_library.py`. The next research step is to decide which prototype formulas are acceptable and which ones should be replaced with more formal definitions.

### Step 2: Add Allocation Logic

After several strategies are fully implemented, add a formal allocation layer:

- equal weight
- volatility parity
- risk parity
- constrained optimizer

### Step 3: Improve Dashboard Interpretation

Add clear flags:

- engine status
- signal maturity
- data source
- last run date
- Yahoo vs synthetic data

## 16. Summary

The project should proceed one layer at a time:

1. Get the dashboard structure working.
2. Get the data pipeline working.
3. Get all 20 prototype strategies working end-to-end.
4. Refine signal formulas and allocation logic.
5. Add allocation and risk controls.
6. Add production data sources and news.

The current system has reached step 3 for all 20 prototype strategies. The next most logical implementation step is reviewing signal quality and adding a formal allocation layer.
