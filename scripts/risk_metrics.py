"""Risk and portfolio math used by the dashboard builder."""

from __future__ import annotations

from math import sqrt
from statistics import mean, pstdev


TRADING_DAYS = 252


def sharpe(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0
    vol = pstdev(returns)
    if vol == 0:
        return 0.0
    return mean(returns) / vol * sqrt(TRADING_DAYS)


def drawdown(nav_series: list[float]) -> float:
    peak = nav_series[0]
    worst = 0.0
    for value in nav_series:
        peak = max(peak, value)
        worst = min(worst, value / peak - 1)
    return worst


def var_es(pnls: list[float], pct_index: int = 1) -> tuple[float, float]:
    ordered = sorted(pnls)
    var = ordered[min(pct_index, len(ordered) - 1)]
    tail = ordered[: pct_index + 1]
    return var, mean(tail)


def covariance(x: list[float], y: list[float]) -> float:
    mx, my = mean(x), mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / len(x)


def beta(y: list[float], x: list[float]) -> float:
    var_x = covariance(x, x)
    if var_x == 0:
        return 0.0
    return covariance(y, x) / var_x


def factor_betas(strategy_returns: list[float], factor_returns: dict[str, list[float]]) -> dict[str, float]:
    return {name: beta(strategy_returns, series) for name, series in factor_returns.items()}


def status_from_limits(
    weight: float,
    strategy_drawdown: float,
    strategy_sharpe: float,
    cost_bps: float = 0.0,
) -> str:
    """Classify current live-style risk from recent metrics.

    Hard breaches still get immediate attention. Milder issues become a breach
    only when more than one risk dimension is flashing at the same time.
    """
    hard_breach = weight > 10 or strategy_drawdown <= -20
    if hard_breach:
        return "Breach"

    warnings = [
        weight > 8,
        strategy_drawdown <= -10,
        strategy_sharpe < 0.5,
        cost_bps > 2.0,
    ]
    warning_count = sum(1 for flag in warnings if flag)
    if strategy_drawdown <= -15 and warning_count >= 2:
        return "Breach"
    if warning_count >= 3:
        return "Breach"
    if warning_count >= 1:
        return "Warning"
    return "Healthy"


def action_from_status(status: str, strategy_sharpe: float, cost_bps: float, strategy_drawdown: float = 0.0) -> str:
    if status == "Breach" and strategy_drawdown <= -20:
        return "Pause"
    if status == "Breach":
        return "Reduce"
    if status == "Warning" and cost_bps > 2.0 and strategy_sharpe < 0.5:
        return "Reduce"
    if status == "Warning":
        return "Rebalance"
    if strategy_sharpe > 1.2 and strategy_drawdown > -8 and cost_bps <= 2.0:
        return "Increase"
    return "Hold"


def factor_status(value: float, limit: float) -> str:
    ratio = abs(value) / limit if limit else 0
    if ratio > 1.25:
        return "Breach"
    if ratio > 0.85:
        return "Warning"
    return "Healthy"
