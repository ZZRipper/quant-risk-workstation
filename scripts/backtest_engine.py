"""Generic backtest engine for stock-level alpha strategies."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from risk_metrics import drawdown, sharpe


BUY_COST_BPS = 5
SELL_COST_BPS = 5


@dataclass
class BacktestResult:
    strategy_id: str
    name: str
    sleeve: str
    description: str
    holdings: list[str]
    dates: list[str]
    daily_returns: list[float]
    daily_pnls: list[float]
    daily_costs: list[float]
    nav_series: list[float]
    turnover: list[float]
    latest_weights: dict[str, float]
    signal_score: int
    sharpe: float
    drawdown: float


def top_n_equal_weight(scores: dict[str, float], top_n: int = 10, max_weight: float = 0.25) -> dict[str, float]:
    """Select the top-scoring names and assign equal long-only weights."""
    if not scores:
        return {}
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    selected = [ticker for ticker, _score in ranked[:top_n]]
    if not selected:
        return {}
    equal_weight = min(1 / len(selected), max_weight)
    weights = {ticker: equal_weight for ticker in selected}
    total = sum(weights.values())
    return {ticker: weight / total for ticker, weight in weights.items()}


def normalize_long_only(scores: dict[str, float], max_weight: float = 0.25) -> dict[str, float]:
    """Convert raw scores into long-only weights with a simple max-weight cap."""
    if not scores:
        return {}
    min_score = min(scores.values())
    shifted = {ticker: score - min_score + 1e-9 for ticker, score in scores.items()}
    total = sum(shifted.values())
    if total <= 0:
        weights = {ticker: 1 / len(scores) for ticker in scores}
    else:
        weights = {ticker: score / total for ticker, score in shifted.items()}

    capped = {ticker: min(weight, max_weight) for ticker, weight in weights.items()}
    capped_total = sum(capped.values())
    if capped_total == 0:
        return {ticker: 1 / len(capped) for ticker in capped}
    return {ticker: weight / capped_total for ticker, weight in capped.items()}


def transaction_cost(prev_weights: dict[str, float], target_weights: dict[str, float], capital: float) -> tuple[float, float]:
    tickers = set(prev_weights) | set(target_weights)
    buy_notional = 0.0
    sell_notional = 0.0
    for ticker in tickers:
        diff = target_weights.get(ticker, 0.0) - prev_weights.get(ticker, 0.0)
        if diff > 0:
            buy_notional += diff * capital
        else:
            sell_notional += abs(diff) * capital
    cost = buy_notional * BUY_COST_BPS / 10_000 + sell_notional * SELL_COST_BPS / 10_000
    turnover = (buy_notional + sell_notional) / capital if capital else 0.0
    return cost, turnover


def run_backtest(strategy, market_data, capital: float, top_n: int = 10) -> BacktestResult:
    """Run a long-only daily-rebalanced strategy.

    Timing convention:
    - `day` is the return earned from prior close to current close.
    - `strategy.signal(market_data, day)` may only use observations before
      `day`, because helper windows slice data as `[:day]`.
    - Signals computed with data through day t-1 determine day t holdings.
    - If a strategy needs more history than is available, the engine stays in
      cash and records zero return/cost for that day.

    The strategy object must expose:
    - id, name, sleeve, description, holdings
    - signal(market_data, day) -> dict[ticker, score]
    """
    nav = [capital]
    daily_returns = []
    daily_pnls = []
    daily_costs = []
    turnover_series = []
    prev_weights = {ticker: 0.0 for ticker in strategy.holdings}
    latest_weights = prev_weights

    for day in range(len(market_data.dates)):
        if day < getattr(strategy, "min_history", 1):
            target_weights = {ticker: 0.0 for ticker in strategy.holdings}
        else:
            scores = strategy.signal(market_data, day)
            target_weights = top_n_equal_weight(scores, top_n=top_n, max_weight=strategy.max_weight)
        cost, day_turnover = transaction_cost(prev_weights, target_weights, nav[-1])
        gross_return = sum(
            target_weights.get(ticker, 0.0) * market_data.stock_returns[ticker][day]
            for ticker in target_weights
        )
        pnl = nav[-1] * gross_return - cost
        net_return = pnl / nav[-1] if nav[-1] else 0.0

        nav.append(nav[-1] + pnl)
        daily_returns.append(net_return)
        daily_pnls.append(pnl)
        daily_costs.append(cost)
        turnover_series.append(day_turnover)
        prev_weights = target_weights
        latest_weights = target_weights

    signal_score = round(max(5, min(95, 50 + sharpe(daily_returns) * 10 - abs(drawdown(nav) * 100))))
    return BacktestResult(
        strategy_id=strategy.id,
        name=strategy.name,
        sleeve=strategy.sleeve,
        description=strategy.description,
        holdings=strategy.holdings,
        dates=market_data.dates,
        daily_returns=daily_returns,
        daily_pnls=daily_pnls,
        daily_costs=daily_costs,
        nav_series=nav,
        turnover=turnover_series,
        latest_weights=latest_weights,
        signal_score=signal_score,
        sharpe=sharpe(daily_returns),
        drawdown=drawdown(nav) * 100,
    )


def summarize_turnover(result: BacktestResult) -> float:
    return mean(result.turnover) * 100 if result.turnover else 0.0
