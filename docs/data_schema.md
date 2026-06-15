# Multi-Strategy Risk Dashboard Data Schema

This dashboard monitors stock-level alpha strategies. ETFs are used only as benchmark and risk-proxy instruments.

## Portfolio Assumptions

- Start date: 2026-06-09
- Initial capital: 1,000,000 USD
- Transaction cost:
  - Buy: 5 bps of buy notional
  - Sell: 5 bps of sell notional
  - Round trip: 10 bps

## Core Formulas

```text
Daily PnL = sum(position_shares * price_change) - transaction_cost

Transaction cost = buy_notional * 0.0005 + sell_notional * 0.0005

NAV_t = NAV_(t-1) + Daily PnL_t

Daily return_t = Daily PnL_t / NAV_(t-1)

Cumulative return_t = NAV_t / initial_capital - 1

Drawdown_t = NAV_t / rolling_max_NAV_t - 1

Sharpe = mean(daily_return) / std(daily_return) * sqrt(252)
```

## Factor Loading

Factor loading is shown as beta.

Simple interpretation:

```text
Strategy return = alpha + beta_factor * factor_return + residual
```

For example:

- Market beta 0.30 means the strategy tends to move 0.30% when the market factor moves 1%.
- Negative USD beta means the strategy tends to benefit when the dollar weakens.
- Credit beta measures sensitivity to credit-spread proxy returns.

## Risk Limits

Limits are intentionally simple and explainable.

| Control | Healthy | Warning | Breach |
|---|---:|---:|---:|
| Strategy weight | <= 8% | > 8% | > 10% |
| Strategy drawdown | > -8% | <= -8% | <= -12% |
| Rolling Sharpe | >= 0.25 | < 0.25 | < -0.50 |
| Pairwise strategy correlation | <= 0.65 | > 0.65 | > 0.80 |
| Market beta | <= 0.30 | > 0.30 | > 0.45 |
| Single macro factor beta | <= 0.20 | > 0.20 | > 0.35 |
| Cost drag monthly | <= 10 bps | > 10 bps | > 20 bps |

## JSON Files

### `portfolio.json`

```json
{
  "nav": 1005131,
  "dailyPnl": -2680,
  "inceptionPnl": 5131,
  "sharpe": 0.65,
  "drawdown": -6.03,
  "var95": -14987,
  "es95": -21433,
  "turnover": 7.8,
  "costDragBps": 0.06,
  "regime": "Risk-on, concentration watch"
}
```

### `strategies.json`

Each row is one stock-level alpha strategy.

```json
{
  "id": "STR-01",
  "name": "WQ Alpha 001 - Short-Term Reversal",
  "sleeve": "Reversal",
  "weight": 5.0,
  "targetWeight": 5.0,
  "capital": 50000,
  "holdings": "AAPL, MSFT, NVDA, AMZN, META",
  "pnl": 1250,
  "sharpe": 1.10,
  "drawdown": -3.4,
  "signal": 76,
  "costBps": 0.05,
  "status": "Healthy",
  "action": "Hold"
}
```

### `factor_exposures.json`

```json
{
  "name": "Market beta",
  "value": 0.28,
  "limit": 0.30,
  "status": "Healthy"
}
```

### `risk_proxies.json`

ETF proxies are not strategies. They are used for benchmark comparison and factor interpretation.

```json
{
  "ticker": "SPY",
  "factor": "Market beta",
  "purpose": "Broad U.S. equity benchmark",
  "loading": 0.28,
  "use": "Compare stock strategy returns against market beta"
}
```

### `market_news.json`

```json
{
  "time": "10:21 AM",
  "source": "News API placeholder",
  "headline": "Semiconductor leadership remains concentrated.",
  "tickers": "NVDA, AVGO, AMD",
  "impact": "High"
}
```

### `macro_regime.json`

```json
{
  "source": "FRED + Yahoo ETF proxy",
  "quadrant": "Falling growth + rising inflation",
  "businessCycle": "Contraction",
  "riskTone": "Stagflation risk",
  "growth": {"direction": "Falling", "score": -0.012},
  "inflation": {"direction": "Rising", "score": 0.018},
  "stress": {"direction": "Rising", "score": 0.006},
  "guidance": [
    {
      "sleeve": "Low Vol / Quality",
      "tilt": "Prefer",
      "reason": "Weakening growth with inflation pressure argues for defensive exposure."
    }
  ]
}
```

### `strategy_validation.json`

```json
{
  "id": "STR-02",
  "name": "WQ Alpha 004 - Rank Momentum",
  "signal": "Rank momentum = trailing 60-day cumulative return.",
  "dataFields": "Close-to-close returns",
  "backtestStart": "2025-12-10",
  "backtestEnd": "2026-06-09",
  "latestHoldings": "NVDA, AVGO, MSFT, META, AMZN, GOOGL, LLY, JPM, COST, HD",
  "annualReturn": 8.4,
  "annualVol": 12.3,
  "sharpe": 0.68,
  "maxDrawdown": -3.2,
  "hitRate": 52.4,
  "avgTurnover": 18.5,
  "avgDailyCostBps": 0.06,
  "totalCostBps": 7.1,
  "macroFit": "Prefer",
  "validationStatus": "Watch",
  "validationReason": "Performance is acceptable but not strong enough for approval without further testing."
}
```

`latestHoldings` is the latest top-N selection from the shared S&P 100-style large-cap universe. The timing convention is:

```text
t-1 signal ranking -> day t top-N equal-weight holdings -> day t PnL
```

### `strategy_correlation.json`

```json
{
  "method": "Pearson correlation",
  "windowDays": 63,
  "actualWindowDays": 63,
  "timing": "Completed daily strategy returns only",
  "purpose": "Risk monitoring and diversification review; not signal generation",
  "asOf": "2026-06-09",
  "labels": ["STR-01", "STR-02"],
  "matrix": [[1.0, 0.42], [0.42, 1.0]],
  "highCorrelationPairs": []
}
```

The dashboard displays the rolling realized correlation window explicitly:

```text
Rolling 63D correlation · completed daily strategy returns · latest market close
```

## Next Integration Steps

1. Use Yahoo Finance or another approved source for real adjusted close data.
2. Review the 20 prototype signals and replace any formula that needs a stricter alpha definition.
3. Recompute daily positions, PnL, transaction costs, NAV, drawdown, Sharpe and beta exposures.
4. Replace placeholder news with an approved market-news API.
5. Upgrade macro regime from ETF proxy fallback to point-in-time macro data when available.
