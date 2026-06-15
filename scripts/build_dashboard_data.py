#!/usr/bin/env python3
"""Build dashboard JSON files for the risk workstation.

This is the pipeline orchestrator:
1. Load market data.
2. Build stock-level alpha strategy returns.
3. Calculate portfolio NAV, PnL, risk metrics and factor betas.
4. Write frontend-ready JSON files.

Current data uses Yahoo Finance when available, with a deterministic synthetic
fallback so the dashboard remains runnable offline.
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

from backtest_engine import run_backtest
from fetch_market_data import LARGE_CAP_UNIVERSE, RISK_PROXIES, load_market_data, load_market_news
from macro_regime import build_macro_regime
from risk_metrics import (
    action_from_status,
    drawdown,
    factor_betas,
    factor_status,
    sharpe,
    status_from_limits,
    var_es,
)
from strategy_correlation import build_strategy_correlation
from strategy_validation import build_strategy_validation, write_validation_report
from strategy_library import STRATEGY_SPECS, build_strategy_objects


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
INITIAL_CAPITAL = 1_000_000
BUY_COST_BPS = 5
SELL_COST_BPS = 5
TARGET_WEIGHT = 5.0
BACKTEST_DAYS = 1260
TOP_N_HOLDINGS = 10
CORRELATION_WINDOW_DAYS = 63
RISK_STATUS_WINDOW_DAYS = 126


FACTOR_LIMITS = {
    "Market beta": 0.30,
    "Size beta": 0.20,
    "Value beta": 0.20,
    "Momentum beta": 0.25,
    "Rates beta": 0.20,
    "Credit beta": 0.20,
    "Volatility beta": 0.20,
    "USD beta": 0.20,
    "Commodity beta": 0.20,
}


PROXY_LOADING_MAP = {
    "SPY": "Market beta",
    "QQQ": "Momentum beta",
    "IWM": "Size beta",
    "TLT": "Rates beta",
    "HYG": "Credit beta",
    "LQD": "Credit beta",
    "GLD": "Commodity beta",
    "DBC": "Commodity beta",
    "UUP": "USD beta",
}


def write_json(name: str, data: object) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_nav(strategy_returns: list[list[float]], weights: list[float]) -> tuple[list[float], list[float], list[float], list[float]]:
    days = len(strategy_returns[0])
    net_nav = [INITIAL_CAPITAL]
    gross_nav = [INITIAL_CAPITAL]
    daily_pnls = []
    daily_costs = []

    for day in range(days):
        weighted_return = sum(weights[i] / 100 * strategy_returns[i][day] for i in range(len(weights)))
        turnover = 0.06 + (day % 5) * 0.01
        cost = net_nav[-1] * turnover * ((BUY_COST_BPS + SELL_COST_BPS) / 2) / 10_000
        pnl = net_nav[-1] * weighted_return - cost
        daily_pnls.append(pnl)
        daily_costs.append(cost)
        gross_nav.append(gross_nav[-1] * (1 + weighted_return))
        net_nav.append(net_nav[-1] + pnl)

    daily_returns = [pnl / nav for pnl, nav in zip(daily_pnls, net_nav[:-1])]
    return net_nav, gross_nav, daily_pnls, daily_costs, daily_returns


def build_market_cards(data_source: str) -> list[dict[str, str]]:
    return [
        {"asset": "Data source", "state": data_source.title(), "value": "Auto loader", "note": "Yahoo Finance first; synthetic fallback if unavailable"},
        {"asset": "Equity", "state": "Risk-on", "value": "+0.8%", "note": "Large-cap breadth is constructive; market beta near warning band"},
        {"asset": "Rates", "state": "Neutral", "value": "-4 bps", "note": "Rates beta is inside limit"},
        {"asset": "Credit", "state": "Watch", "value": "+7 bps", "note": "Credit beta is moderate; watch cyclical stock baskets"},
        {"asset": "FX", "state": "USD firm", "value": "+0.3%", "note": "USD beta is slightly negative"},
        {"asset": "Commodities", "state": "Mixed", "value": "-0.4%", "note": "Commodity beta is inside limit"},
        {"asset": "Volatility", "state": "Elevated", "value": "VIX 18.7", "note": "Vol beta close to warning band"},
        {"asset": "Macro", "state": "Event risk", "value": "CPI pending", "note": "Avoid high-turnover rebalance before release"},
        {"asset": "ETF proxies", "state": "Coverage OK", "value": "9 proxies", "note": "Used only for benchmark and factor comparison"},
    ]


def build() -> None:
    market_data = load_market_data(days=BACKTEST_DAYS, source="auto")
    macro_regime = build_macro_regime(market_data)
    weights = [5.2, 5.4, 4.9, 5.0, 4.6, 5.5, 4.8, 5.1, 4.4, 4.7, 5.0, 4.8, 4.5, 5.3, 4.9, 5.2, 4.6, 5.1, 4.7, 4.3]

    strategy_universe = list(market_data.stock_returns.keys())
    strategy_objects = build_strategy_objects(strategy_universe)
    backtest_results = {
        idx: run_backtest(strategy_objects[idx], market_data, INITIAL_CAPITAL * weights[idx] / 100, top_n=TOP_N_HOLDINGS)
        for idx in range(len(strategy_objects))
    }

    strategy_returns = [backtest_results[idx].daily_returns for idx in range(len(STRATEGY_SPECS))]
    strategy_holdings = [list(backtest_results[idx].latest_weights.keys()) for idx in range(len(STRATEGY_SPECS))]

    net_nav, _gross_nav, daily_pnls, daily_costs, portfolio_returns = build_nav(strategy_returns, weights)
    portfolio_factor_betas = factor_betas(portfolio_returns, market_data.factor_returns)

    strategies = []
    for idx, spec in enumerate(STRATEGY_SPECS):
        capital = INITIAL_CAPITAL * weights[idx] / 100
        result = backtest_results[idx]
        pnls = result.daily_pnls
        recent_returns = result.daily_returns[-RISK_STATUS_WINDOW_DAYS:]
        recent_nav = result.nav_series[-(RISK_STATUS_WINDOW_DAYS + 1):]
        recent_costs = result.daily_costs[-RISK_STATUS_WINDOW_DAYS:]
        strategy_sharpe = sharpe(recent_returns)
        strategy_drawdown = drawdown(recent_nav) * 100
        full_period_sharpe = result.sharpe
        full_period_drawdown = result.drawdown
        cost_bps = (sum(recent_costs) / len(recent_costs)) / capital * 10_000 if capital and recent_costs else 0.0
        status = status_from_limits(weights[idx], strategy_drawdown, strategy_sharpe, cost_bps)
        action = action_from_status(status, strategy_sharpe, cost_bps, strategy_drawdown)
        signal = result.signal_score
        description = result.description + f" Status uses rolling {RISK_STATUS_WINDOW_DAYS}D risk metrics; validation still tracks full-period backtest."

        strategies.append({
            "id": f"STR-{idx + 1:02d}",
            "name": spec.name,
            "sleeve": spec.sleeve,
            "description": description,
            "weight": round(weights[idx], 2),
            "targetWeight": TARGET_WEIGHT,
            "capital": round(capital, 2),
            "holdings": ", ".join(strategy_holdings[idx]),
            "holdingRule": f"S&P 100-style shared universe; t-1 signal selects top {TOP_N_HOLDINGS}; equal weight",
            "pnl": round(pnls[-1], 2),
            "sharpe": round(strategy_sharpe, 2),
            "drawdown": round(strategy_drawdown, 2),
            "fullPeriodSharpe": round(full_period_sharpe, 2),
            "fullPeriodDrawdown": round(full_period_drawdown, 2),
            "riskWindowDays": RISK_STATUS_WINDOW_DAYS,
            "signal": signal,
            "costBps": round(cost_bps, 3),
            "status": status,
            "action": action,
            "engine": "backtest_engine",
        })

    factors = []
    for name, limit in FACTOR_LIMITS.items():
        value = portfolio_factor_betas.get(name, 0.0)
        factors.append({
            "name": name,
            "value": round(value, 3),
            "limit": limit,
            "status": factor_status(value, limit),
        })

    proxies = []
    for proxy in RISK_PROXIES:
        factor_name = PROXY_LOADING_MAP[proxy["ticker"]]
        proxies.append({
            **proxy,
            "loading": round(portfolio_factor_betas.get(factor_name, 0.0), 3),
        })

    portfolio_var, portfolio_es = var_es(daily_pnls)
    portfolio = {
        "nav": round(net_nav[-1], 2),
        "dailyPnl": round(daily_pnls[-1], 2),
        "inceptionPnl": round(net_nav[-1] - INITIAL_CAPITAL, 2),
        "sharpe": round(sharpe(portfolio_returns), 2),
        "drawdown": round(drawdown(net_nav) * 100, 2),
        "var95": round(portfolio_var, 2),
        "es95": round(portfolio_es, 2),
        "turnover": round(mean([0.06 + (day % 5) * 0.01 for day in range(len(daily_pnls))]) * 100, 2),
        "costDragBps": round(sum(daily_costs) / INITIAL_CAPITAL * 10_000, 2),
        "regime": macro_regime["riskTone"],
        "universeName": "S&P 100-style large-cap universe",
        "universeSize": len(strategy_universe),
        "candidateUniverseSize": len(LARGE_CAP_UNIVERSE),
    }
    validation_rows = build_strategy_validation(strategies, backtest_results, market_data, macro_regime)
    strategy_correlation = build_strategy_correlation(
        strategies,
        strategy_returns,
        market_data.dates,
        window_days=CORRELATION_WINDOW_DAYS,
    )

    write_json("portfolio.json", portfolio)
    write_json("strategies.json", strategies)
    write_json("strategy_validation.json", validation_rows)
    write_json("strategy_correlation.json", strategy_correlation)
    write_json("factor_exposures.json", factors)
    write_json("risk_proxies.json", proxies)
    write_json("nav_series.json", [round(value, 2) for value in net_nav])
    market_cards = build_market_cards(market_data.source)
    write_json("market.json", market_cards)
    write_json("market_news.json", load_market_news())
    write_json("macro_regime.json", macro_regime)
    write_validation_report(validation_rows, macro_regime, REPORTS_DIR / "strategy_validation_report.md")

    bundle = {
        "portfolio": portfolio,
        "strategies": strategies,
        "strategyValidation": validation_rows,
        "strategyCorrelation": strategy_correlation,
        "factorExposures": factors,
        "riskProxies": proxies,
        "navSeries": [round(value, 2) for value in net_nav],
        "market": market_cards,
        "marketNews": load_market_news(),
        "macroRegime": macro_regime,
    }
    (DATA_DIR / "data_bundle.js").write_text(
        "window.DASHBOARD_DATA = " + json.dumps(bundle, indent=2) + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    build()
    print(f"Wrote dashboard data to {DATA_DIR}")
