"""WorldQuant-style strategy definitions and alpha signal logic."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import pstdev


@dataclass(frozen=True)
class StrategySpec:
    name: str
    sleeve: str
    explanation: str


@dataclass
class Strategy:
    id: str
    name: str
    sleeve: str
    description: str
    holdings: list[str]
    max_weight: float = 0.25
    min_history = 1

    def signal(self, market_data, day: int) -> dict[str, float]:
        raise NotImplementedError


class ShortTermReversalStrategy(Strategy):
    lookback: int = 5
    min_history = 5

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_sum_window(market_data.stock_returns[ticker], day, self.lookback)
            for ticker in self.holdings
        }


class RankMomentumStrategy(Strategy):
    lookback: int = 60
    min_history = 60

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, self.lookback)
            for ticker in self.holdings
        }


class VolumePriceDivergenceStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 5) * _volume_ratio(market_data.stock_volume[ticker], day, 20)
            for ticker in self.holdings
        }


class OpenClosePressureStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _latest(market_data.stock_returns[ticker], day) - _mean_window(market_data.stock_returns[ticker], day, 20)
            for ticker in self.holdings
        }


class TrendStabilityStrategy(Strategy):
    min_history = 40

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 40) - 3 * _vol_window(market_data.stock_returns[ticker], day, 40)
            for ticker in self.holdings
        }


class DelayedMomentumStrategy(Strategy):
    min_history = 45

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _lagged_sum_window(market_data.stock_returns[ticker], day, window=40, lag=5)
            for ticker in self.holdings
        }


class CorrelationReversalStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_corr_window(market_data.stock_returns[ticker], _pct_change_series(market_data.stock_volume[ticker]), day, 20)
            for ticker in self.holdings
        }


class VwapMeanReversionStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_price_deviation(market_data.stock_close[ticker], day, 20)
            for ticker in self.holdings
        }


class HighLowRangeStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_range_ratio(market_data.stock_high[ticker], market_data.stock_low[ticker], market_data.stock_close[ticker], day, 20)
            for ticker in self.holdings
        }


class VolumeAccelerationStrategy(Strategy):
    min_history = 30

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 5)
            * (_volume_ratio(market_data.stock_volume[ticker], day, 5) - _volume_ratio(market_data.stock_volume[ticker], day, 30))
            for ticker in self.holdings
        }


class DecayMomentumStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _decay_weighted_sum(market_data.stock_returns[ticker], day, 20)
            for ticker in self.holdings
        }


class TurnoverReversalStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_sum_window(market_data.stock_returns[ticker], day, 5) * _volume_ratio(market_data.stock_volume[ticker], day, 20)
            for ticker in self.holdings
        }


class PriceVolumeRankStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 10)
            + 0.01 * (_volume_ratio(market_data.stock_volume[ticker], day, 20) - 1)
            for ticker in self.holdings
        }


class CompositeRankStrategy(Strategy):
    min_history = 30

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 30)
            - _sum_window(market_data.stock_returns[ticker], day, 5)
            - 2 * _vol_window(market_data.stock_returns[ticker], day, 30)
            for ticker in self.holdings
        }


class CorrelationBreakStrategy(Strategy):
    min_history = 40

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: abs(
                _corr_window(market_data.stock_returns[ticker], _pct_change_series(market_data.stock_volume[ticker]), day, 10)
                - _corr_window(market_data.stock_returns[ticker], _pct_change_series(market_data.stock_volume[ticker]), day, 40)
            )
            for ticker in self.holdings
        }


class RangeMomentumStrategy(Strategy):
    min_history = 20

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 15)
            * max(0.0, _range_ratio(market_data.stock_high[ticker], market_data.stock_low[ticker], market_data.stock_close[ticker], day, 20))
            for ticker in self.holdings
        }


class LiquidityAdjustedMomentumStrategy(Strategy):
    min_history = 30

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 30)
            / max(_volume_ratio(market_data.stock_volume[ticker], day, 20), 0.25)
            for ticker in self.holdings
        }


class DelayedReversalStrategy(Strategy):
    min_history = 25

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_lagged_sum_window(market_data.stock_returns[ticker], day, window=20, lag=5)
            for ticker in self.holdings
        }


class RiskControlledMomentumStrategy(Strategy):
    min_history = 60

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: _sum_window(market_data.stock_returns[ticker], day, 60)
            / max(_vol_window(market_data.stock_returns[ticker], day, 60), 0.0001)
            for ticker in self.holdings
        }


class CloseToOpenReversalStrategy(Strategy):
    min_history = 1

    def signal(self, market_data, day: int) -> dict[str, float]:
        return {
            ticker: -_latest(market_data.stock_returns[ticker], day)
            for ticker in self.holdings
        }


STRATEGY_SPECS = [
    StrategySpec("WQ Alpha 001 - Short-Term Reversal", "Reversal", "Ranks recent losers for possible short-term rebound."),
    StrategySpec("WQ Alpha 004 - Rank Momentum", "Momentum", "Ranks stocks by recent relative strength."),
    StrategySpec("WQ Alpha 006 - Volume Price Divergence", "Volume", "Looks for price moves confirmed or rejected by volume."),
    StrategySpec("WQ Alpha 012 - Open-Close Pressure", "Intraday", "Uses open-to-close behavior as a pressure signal."),
    StrategySpec("WQ Alpha 021 - Trend Stability", "Trend", "Rewards stable trend persistence."),
    StrategySpec("WQ Alpha 024 - Delayed Momentum", "Momentum", "Uses lagged momentum to reduce immediate reversal risk."),
    StrategySpec("WQ Alpha 028 - Correlation Reversal", "Correlation", "Looks for unstable price-volume co-movement."),
    StrategySpec("WQ Alpha 032 - VWAP Mean Reversion", "Reversion", "Compares price to VWAP-style fair value."),
    StrategySpec("WQ Alpha 041 - High-Low Range", "Volatility", "Uses daily range information to detect risk pressure."),
    StrategySpec("WQ Alpha 043 - Volume Acceleration", "Volume", "Detects changes in liquidity and participation."),
    StrategySpec("WQ Alpha 051 - Decay Momentum", "Momentum", "Uses decayed ranked returns."),
    StrategySpec("WQ Alpha 055 - Turnover Reversal", "Liquidity", "Pairs turnover spikes with reversal logic."),
    StrategySpec("WQ Alpha 060 - Price Volume Rank", "Volume", "Cross-sectional rank of price-volume interaction."),
    StrategySpec("WQ Alpha 071 - Composite Rank", "Composite", "Combines several rank-based technical components."),
    StrategySpec("WQ Alpha 078 - Correlation Break", "Correlation", "Detects recent correlation breakdowns."),
    StrategySpec("WQ Alpha 083 - Range Momentum", "Volatility", "Combines range expansion with momentum."),
    StrategySpec("WQ Alpha 088 - Liquidity Adjusted Momentum", "Liquidity", "Momentum adjusted for trading activity."),
    StrategySpec("WQ Alpha 092 - Delayed Reversal", "Reversal", "Uses delayed price action for mean reversion."),
    StrategySpec("WQ Alpha 096 - Risk Controlled Momentum", "Momentum", "Momentum signal penalized by volatility."),
    StrategySpec("WQ Alpha 101 - Close To Open Reversal", "Intraday", "Uses close-to-open behavior as an overnight reversal signal."),
]


STRATEGY_CLASS_BY_INDEX = [
    ShortTermReversalStrategy,
    RankMomentumStrategy,
    VolumePriceDivergenceStrategy,
    OpenClosePressureStrategy,
    TrendStabilityStrategy,
    DelayedMomentumStrategy,
    CorrelationReversalStrategy,
    VwapMeanReversionStrategy,
    HighLowRangeStrategy,
    VolumeAccelerationStrategy,
    DecayMomentumStrategy,
    TurnoverReversalStrategy,
    PriceVolumeRankStrategy,
    CompositeRankStrategy,
    CorrelationBreakStrategy,
    RangeMomentumStrategy,
    LiquidityAdjustedMomentumStrategy,
    DelayedReversalStrategy,
    RiskControlledMomentumStrategy,
    CloseToOpenReversalStrategy,
]


def holdings_for_strategy(universe: list[str], strategy_idx: int, size: int = 5) -> list[str]:
    """Return the shared investable universe for every strategy.

    The backtest engine selects the latest top-N holdings from this shared
    universe using each strategy's t-1 signal.
    """
    return list(universe)


def build_strategy_objects(universe: list[str]) -> list[Strategy]:
    strategies: list[Strategy] = []
    for idx, spec in enumerate(STRATEGY_SPECS):
        base = {
            "id": f"STR-{idx + 1:02d}",
            "name": spec.name,
            "sleeve": spec.sleeve,
            "description": spec.explanation,
            "holdings": holdings_for_strategy(universe, idx),
        }
        strategies.append(STRATEGY_CLASS_BY_INDEX[idx](**base))
    return strategies


def _latest(values: list[float], end: int) -> float:
    idx = max(0, min(end - 1, len(values) - 1))
    return values[idx] if values else 0.0


def _sum_window(values: list[float], end: int, window: int) -> float:
    start = max(0, end - window)
    return sum(values[start:end])


def _lagged_sum_window(values: list[float], end: int, window: int, lag: int) -> float:
    lagged_end = max(0, end - lag)
    return _sum_window(values, lagged_end, window)


def _mean_window(values: list[float], end: int, window: int) -> float:
    start = max(0, end - window)
    sample = values[start:end]
    return sum(sample) / len(sample) if sample else 0.0


def _vol_window(values: list[float], end: int, window: int) -> float:
    start = max(0, end - window)
    sample = values[start:end]
    return pstdev(sample) if len(sample) > 1 else 0.0


def _decay_weighted_sum(values: list[float], end: int, window: int) -> float:
    start = max(0, end - window)
    sample = values[start:end]
    total_weight = sum(range(1, len(sample) + 1))
    if total_weight == 0:
        return 0.0
    return sum(value * weight for weight, value in enumerate(sample, start=1)) / total_weight


def _pct_change_series(values: list[float]) -> list[float]:
    changes = [0.0]
    for prev, current in zip(values, values[1:]):
        changes.append((current - prev) / prev if prev else 0.0)
    return changes


def _corr_window(left: list[float], right: list[float], end: int, window: int) -> float:
    start = max(0, end - window)
    left_sample = left[start:end]
    right_sample = right[start:end]
    if len(left_sample) < 3 or len(left_sample) != len(right_sample):
        return 0.0
    left_mean = sum(left_sample) / len(left_sample)
    right_mean = sum(right_sample) / len(right_sample)
    left_dev = [value - left_mean for value in left_sample]
    right_dev = [value - right_mean for value in right_sample]
    left_var = sum(value * value for value in left_dev)
    right_var = sum(value * value for value in right_dev)
    if left_var == 0 or right_var == 0:
        return 0.0
    return sum(a * b for a, b in zip(left_dev, right_dev)) / (left_var * right_var) ** 0.5


def _volume_ratio(volume: list[float], end: int, window: int) -> float:
    current = _latest(volume, end)
    average = _mean_window(volume, end, window)
    return current / average if average else 1.0


def _price_deviation(close: list[float], end: int, window: int) -> float:
    current = _latest(close, end)
    average = _mean_window(close, end, window)
    return (current - average) / average if average else 0.0


def _range_ratio(high: list[float], low: list[float], close: list[float], end: int, window: int) -> float:
    idx = max(0, min(end - 1, len(close) - 1))
    current_close = close[idx] if close else 0.0
    current_range = (high[idx] - low[idx]) / current_close if current_close else 0.0
    ranges = [
        (h - l) / c if c else 0.0
        for h, l, c in zip(high, low, close)
    ]
    average_range = _mean_window(ranges, end, window)
    return current_range / average_range if average_range else 1.0


def _normalize_long_only(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    min_score = min(scores.values())
    shifted = {ticker: score - min_score + 1e-9 for ticker, score in scores.items()}
    total = sum(shifted.values())
    if total == 0:
        return {ticker: 1 / len(scores) for ticker in scores}
    return {ticker: score / total for ticker, score in shifted.items()}


def _portfolio_return(weights: dict[str, float], stock_returns: dict[str, list[float]], day: int) -> float:
    return sum(weight * stock_returns[ticker][day] for ticker, weight in weights.items())


def alpha_short_term_reversal(holdings: list[str], market_data, window: int = 5) -> list[float]:
    returns = []
    days = len(next(iter(market_data.stock_returns.values())))
    for day in range(days):
        scores = {ticker: -_sum_window(market_data.stock_returns[ticker], day, window) for ticker in holdings}
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns


def alpha_momentum(holdings: list[str], market_data, window: int = 60) -> list[float]:
    returns = []
    days = len(next(iter(market_data.stock_returns.values())))
    for day in range(days):
        scores = {ticker: _sum_window(market_data.stock_returns[ticker], day, window) for ticker in holdings}
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns


def alpha_volume_price_confirmation(holdings: list[str], market_data, window: int = 20) -> list[float]:
    returns = []
    days = len(next(iter(market_data.stock_returns.values())))
    for day in range(days):
        scores = {}
        for ticker in holdings:
            recent_ret = _sum_window(market_data.stock_returns[ticker], day, 5)
            avg_volume = _mean_window(market_data.stock_volume[ticker], day, window)
            current_volume = market_data.stock_volume[ticker][day]
            volume_ratio = current_volume / avg_volume if avg_volume else 1.0
            scores[ticker] = recent_ret * volume_ratio
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns


def alpha_low_volatility(holdings: list[str], market_data, window: int = 20) -> list[float]:
    returns = []
    days = len(next(iter(market_data.stock_returns.values())))
    for day in range(days):
        scores = {ticker: -_vol_window(market_data.stock_returns[ticker], day, window) for ticker in holdings}
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns


def alpha_range_breakout(holdings: list[str], market_data, window: int = 20) -> list[float]:
    returns = []
    days = len(next(iter(market_data.stock_returns.values())))
    for day in range(days):
        scores = {}
        for ticker in holdings:
            close = market_data.stock_close[ticker][day]
            daily_range = (market_data.stock_high[ticker][day] - market_data.stock_low[ticker][day]) / close if close else 0
            avg_range = _mean_window(
                [
                    (h - l) / c if c else 0
                    for h, l, c in zip(market_data.stock_high[ticker], market_data.stock_low[ticker], market_data.stock_close[ticker])
                ],
                day,
                window,
            )
            trend = _sum_window(market_data.stock_returns[ticker], day, 10)
            scores[ticker] = trend if daily_range >= avg_range else -abs(trend)
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns


def strategy_return(holdings: list[str], market_data, strategy_idx: int) -> list[float]:
    """Legacy helper that mirrors the strategy object's signal-to-return path."""
    spec = STRATEGY_SPECS[strategy_idx]
    strategy = STRATEGY_CLASS_BY_INDEX[strategy_idx](
        id=f"STR-{strategy_idx + 1:02d}",
        name=spec.name,
        sleeve=spec.sleeve,
        description=spec.explanation,
        holdings=holdings,
    )
    stock_returns = market_data.stock_returns
    days = len(next(iter(stock_returns.values())))
    returns = []
    for day in range(days):
        scores = strategy.signal(market_data, day)
        weights = _normalize_long_only(scores)
        returns.append(_portfolio_return(weights, market_data.stock_returns, day))
    return returns
