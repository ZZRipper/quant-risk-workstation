"""Strategy validation outputs for research review.

This module turns backtest engine results into a research-style validation
table. It is intentionally separate from the dashboard so the same evidence can
be used in reports, supervisor updates and interview explanations.
"""

from __future__ import annotations

from math import sqrt
from pathlib import Path
from statistics import mean, pstdev

from risk_metrics import TRADING_DAYS, factor_betas


SIGNAL_DEFINITIONS = {
    "STR-01": {
        "signal": "Short-term reversal = negative trailing 5-day return.",
        "data": "Close-to-close returns",
        "intuition": "Recent losers may rebound when moves are short-lived.",
    },
    "STR-02": {
        "signal": "Rank momentum = trailing 60-day cumulative return.",
        "data": "Close-to-close returns",
        "intuition": "Stocks with stronger recent relative strength may continue to lead.",
    },
    "STR-03": {
        "signal": "Volume-price divergence = trailing 5-day return multiplied by 20-day volume ratio.",
        "data": "Close-to-close returns, volume",
        "intuition": "Price moves supported by unusual participation may carry more information.",
    },
    "STR-04": {
        "signal": "Open-close pressure proxy = latest return minus trailing 20-day average return.",
        "data": "Close-to-close returns",
        "intuition": "Recent pressure is compared with normal behavior to detect short-term imbalance.",
    },
    "STR-05": {
        "signal": "Trend stability = trailing 40-day return minus volatility penalty.",
        "data": "Close-to-close returns",
        "intuition": "Stable trends are preferred to noisy returns.",
    },
    "STR-06": {
        "signal": "Delayed momentum = 40-day cumulative return, lagged by 5 days.",
        "data": "Close-to-close returns",
        "intuition": "Lagging the signal reduces immediate reversal risk.",
    },
    "STR-07": {
        "signal": "Correlation reversal = negative 20-day return-volume correlation.",
        "data": "Close-to-close returns, volume",
        "intuition": "Unstable price-volume co-movement can indicate a reversal setup.",
    },
    "STR-08": {
        "signal": "VWAP-style mean reversion = negative deviation from 20-day average close.",
        "data": "Close prices",
        "intuition": "Stocks stretched above short-term fair value are penalized.",
    },
    "STR-09": {
        "signal": "High-low range = negative current range relative to trailing average range.",
        "data": "High, low, close",
        "intuition": "Large range expansion can indicate risk pressure rather than clean alpha.",
    },
    "STR-10": {
        "signal": "Volume acceleration = recent return times short-volume ratio minus long-volume ratio.",
        "data": "Close-to-close returns, volume",
        "intuition": "Accelerating participation can confirm or reject recent price moves.",
    },
    "STR-11": {
        "signal": "Decay momentum = recency-weighted 20-day return.",
        "data": "Close-to-close returns",
        "intuition": "More recent returns receive more signal weight.",
    },
    "STR-12": {
        "signal": "Turnover reversal = negative recent return times 20-day volume ratio.",
        "data": "Close-to-close returns, volume",
        "intuition": "High-turnover moves can mean overreaction and later reversal.",
    },
    "STR-13": {
        "signal": "Price-volume rank = 10-day return plus volume-ratio participation adjustment.",
        "data": "Close-to-close returns, volume",
        "intuition": "Combines price strength with trading participation.",
    },
    "STR-14": {
        "signal": "Composite rank = 30-day trend minus 5-day reversal pressure and volatility penalty.",
        "data": "Close-to-close returns",
        "intuition": "Blends medium-term trend, short-term overextension and risk control.",
    },
    "STR-15": {
        "signal": "Correlation break = absolute difference between 10-day and 40-day return-volume correlation.",
        "data": "Close-to-close returns, volume",
        "intuition": "Large correlation shifts can flag changing market microstructure.",
    },
    "STR-16": {
        "signal": "Range momentum = 15-day return multiplied by range expansion.",
        "data": "Close-to-close returns, high, low, close",
        "intuition": "Momentum is emphasized when price range confirms participation.",
    },
    "STR-17": {
        "signal": "Liquidity-adjusted momentum = 30-day momentum divided by volume ratio.",
        "data": "Close-to-close returns, volume",
        "intuition": "Momentum is penalized when it requires unusually high trading activity.",
    },
    "STR-18": {
        "signal": "Delayed reversal = negative 20-day return, lagged by 5 days.",
        "data": "Close-to-close returns",
        "intuition": "A slower reversal signal avoids reacting to the most recent move.",
    },
    "STR-19": {
        "signal": "Risk-controlled momentum = 60-day momentum divided by trailing volatility.",
        "data": "Close-to-close returns",
        "intuition": "Momentum is scaled by realized risk.",
    },
    "STR-20": {
        "signal": "Close-to-open reversal proxy = negative latest return.",
        "data": "Close-to-close returns",
        "intuition": "Very short-term moves may mean revert on the next rebalance.",
    },
}


def _annual_return(returns: list[float]) -> float:
    if not returns:
        return 0.0
    return mean(returns) * TRADING_DAYS


def _annual_vol(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0
    return pstdev(returns) * sqrt(TRADING_DAYS)


def _hit_rate(returns: list[float]) -> float:
    active = [value for value in returns if value != 0]
    if not active:
        return 0.0
    return sum(1 for value in active if value > 0) / len(active)


def _max_abs_factor(strategy_returns: list[float], factor_returns: dict[str, list[float]]) -> tuple[str, float]:
    betas = factor_betas(strategy_returns, factor_returns)
    if not betas:
        return "N/A", 0.0
    name, value = max(betas.items(), key=lambda item: abs(item[1]))
    return name, value


def _macro_fit(sleeve: str, macro_regime: dict[str, object]) -> tuple[str, str]:
    guidance = macro_regime.get("guidance", [])
    sleeve_lower = sleeve.lower()
    for item in guidance:
        label = str(item.get("sleeve", "")).lower()
        if sleeve_lower in label or any(word in label for word in sleeve_lower.split()):
            return str(item.get("tilt", "Neutral")), str(item.get("reason", "Matches current macro guidance."))

    quadrant = str(macro_regime.get("quadrant", ""))
    if sleeve in {"Momentum", "Trend"} and quadrant == "Rising growth + falling inflation":
        return "Prefer", "Momentum and trend sleeves often fit a risk-on disinflationary backdrop."
    if sleeve in {"Volatility", "Reversal"} and "Falling growth" in quadrant:
        return "Watch", "Defensive or reversal sleeves can help, but drawdown control matters in slowing growth."
    if sleeve in {"Volume", "Liquidity"} and "rising inflation" in quadrant:
        return "Watch", "Liquidity-sensitive strategies should be monitored when macro volatility is elevated."
    return "Neutral", "No direct macro-regime preference; evaluate using strategy-level metrics."


def _validation_status(sharpe: float, drawdown: float, avg_daily_cost_bps: float, hit_rate: float) -> tuple[str, str]:
    reasons = []
    if sharpe < -0.5:
        reasons.append("Sharpe is below breach threshold")
    if drawdown <= -8:
        reasons.append("drawdown is beyond watch threshold")
    if avg_daily_cost_bps > 0.20:
        reasons.append("average daily transaction cost is high")
    if hit_rate < 0.45:
        reasons.append("hit rate is weak")
    if sharpe >= 1.0 and drawdown > -5 and avg_daily_cost_bps <= 0.15:
        return "Pass", "Strong risk-adjusted performance with controlled drawdown and cost."
    if reasons:
        status = "Reject" if sharpe < -1.0 or drawdown <= -12 else "Watch"
        return status, "; ".join(reasons) + "."
    return "Watch", "Performance is acceptable but not strong enough for approval without further testing."


def build_strategy_validation(
    strategies: list[dict[str, object]],
    backtest_results: dict[int, object],
    market_data,
    macro_regime: dict[str, object],
) -> list[dict[str, object]]:
    rows = []
    for idx, strategy in enumerate(strategies):
        result = backtest_results[idx]
        returns = result.daily_returns
        factor_name, factor_beta = _max_abs_factor(returns, market_data.factor_returns)
        macro_fit, macro_reason = _macro_fit(str(strategy["sleeve"]), macro_regime)
        annual_return = _annual_return(returns)
        annual_vol = _annual_vol(returns)
        hit_rate = _hit_rate(returns)
        average_turnover = mean(result.turnover) if result.turnover else 0.0
        capital = float(strategy["capital"])
        total_cost_bps = (sum(result.daily_costs) / capital * 10_000) if capital else 0.0
        avg_daily_cost_bps = (mean(result.daily_costs) / capital * 10_000) if capital and result.daily_costs else 0.0
        validation_status, reason = _validation_status(result.sharpe, result.drawdown, avg_daily_cost_bps, hit_rate)
        definition = SIGNAL_DEFINITIONS.get(str(strategy["id"]), {})
        rows.append({
            "id": strategy["id"],
            "name": strategy["name"],
            "sleeve": strategy["sleeve"],
            "signal": definition.get("signal", strategy["description"]),
            "dataFields": definition.get("data", "OHLCV"),
            "intuition": definition.get("intuition", ""),
            "backtestStart": market_data.dates[0],
            "backtestEnd": market_data.dates[-1],
            "observations": len(returns),
            "latestHoldings": strategy["holdings"],
            "annualReturn": round(annual_return * 100, 2),
            "annualVol": round(annual_vol * 100, 2),
            "sharpe": round(result.sharpe, 2),
            "maxDrawdown": round(result.drawdown, 2),
            "hitRate": round(hit_rate * 100, 1),
            "avgTurnover": round(average_turnover * 100, 2),
            "avgDailyCostBps": round(avg_daily_cost_bps, 3),
            "totalCostBps": round(total_cost_bps, 2),
            "dominantFactor": factor_name,
            "dominantFactorBeta": round(factor_beta, 3),
            "macroFit": macro_fit,
            "macroReason": macro_reason,
            "riskStatus": strategy["status"],
            "dashboardAction": strategy["action"],
            "validationStatus": validation_status,
            "validationReason": reason,
        })
    return rows


def write_validation_report(
    rows: list[dict[str, object]],
    macro_regime: dict[str, object],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Strategy Validation Report",
        "",
        "## Scope",
        "",
        "This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.",
        "",
        f"- Macro regime: {macro_regime.get('quadrant', 'N/A')} ({macro_regime.get('riskTone', 'N/A')})",
        f"- Macro source: {macro_regime.get('source', 'N/A')}",
        f"- Fallback note: {macro_regime.get('fallbackReason', 'none')}",
        "",
        "## Validation Table",
        "",
        "| ID | Strategy | Latest Top Holdings | Signal | Data | Sharpe | Max DD | Hit Rate | Avg Cost bps/day | Macro Fit | Status | Reason |",
        "|---|---|---|---|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {id} | {name} | {latestHoldings} | {signal} | {dataFields} | {sharpe:.2f} | {maxDrawdown:.2f}% | {hitRate:.1f}% | {avgDailyCostBps:.3f} | {macroFit} | {validationStatus} | {validationReason} |".format(**row)
        )

    lines.extend([
        "",
        "## Methodology Notes",
        "",
        "- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.",
        "- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.",
        "- The backtest engine stays in cash until each strategy has enough minimum history.",
        "- Current stock allocation inside each strategy is top-N equal weight.",
        "- Transaction costs use 5 bps for buys and 5 bps for sells.",
        "- Current universe and strategy formulas are prototype research assumptions.",
        "- The current public-data version still has survivorship bias because the equity universe is not point-in-time.",
        "- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.",
        "",
    ])
    output_path.write_text("\n".join(lines), encoding="utf-8")
