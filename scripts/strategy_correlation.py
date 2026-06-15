"""Realized strategy correlation utilities."""

from __future__ import annotations

from statistics import mean, pstdev


def _corr(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 3:
        return 0.0
    left_vol = pstdev(left)
    right_vol = pstdev(right)
    if left_vol == 0 or right_vol == 0:
        return 0.0
    left_mean = mean(left)
    right_mean = mean(right)
    cov = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right)) / len(left)
    return cov / (left_vol * right_vol)


def _window(values: list[float], window_days: int) -> list[float]:
    return values[-window_days:] if len(values) >= window_days else values


def build_strategy_correlation(
    strategies: list[dict[str, object]],
    strategy_returns: list[list[float]],
    dates: list[str],
    window_days: int = 63,
) -> dict[str, object]:
    labels = [str(strategy["id"]) for strategy in strategies]
    names = [str(strategy["name"]) for strategy in strategies]
    returns_window = [_window(returns, window_days) for returns in strategy_returns]
    actual_window = min((len(returns) for returns in returns_window), default=0)
    matrix = []
    for left in returns_window:
        row = []
        for right in returns_window:
            row.append(round(_corr(left[-actual_window:], right[-actual_window:]), 3) if actual_window else 0.0)
        matrix.append(row)

    high_pairs = []
    for i, left_label in enumerate(labels):
        for j in range(i + 1, len(labels)):
            value = matrix[i][j]
            if abs(value) >= 0.65:
                high_pairs.append({
                    "leftId": left_label,
                    "leftName": names[i],
                    "rightId": labels[j],
                    "rightName": names[j],
                    "correlation": value,
                    "status": "Breach" if abs(value) >= 0.80 else "Warning",
                })
    high_pairs.sort(key=lambda item: abs(item["correlation"]), reverse=True)

    return {
        "method": "Pearson correlation",
        "windowDays": window_days,
        "actualWindowDays": actual_window,
        "timing": "Completed daily strategy returns only",
        "purpose": "Risk monitoring and diversification review; not signal generation",
        "asOf": dates[-1] if dates else "N/A",
        "labels": labels,
        "names": names,
        "matrix": matrix,
        "highCorrelationPairs": high_pairs[:10],
    }
