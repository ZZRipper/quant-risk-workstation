"""Macro regime classification for the risk workstation.

The first version uses open-access FRED CSV endpoints when available. If FRED
cannot be reached, it falls back to the ETF/factor proxy returns already loaded
for the strategy backtest.
"""

from __future__ import annotations

import csv
import io
from urllib.error import URLError
from urllib.request import urlopen


FRED_SERIES = {
    "INDPRO": "Industrial production",
    "PAYEMS": "Nonfarm payrolls",
    "UNRATE": "Unemployment rate",
    "CPIAUCSL": "CPI",
    "T10YIE": "10Y breakeven inflation",
    "DGS10": "10Y Treasury yield",
    "BAA10YM": "Baa credit spread",
    "VIXCLS": "VIX",
}


def _load_fred_series(series_id: str) -> list[tuple[str, float]]:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        with urlopen(url, timeout=8) as response:
            payload = response.read().decode("utf-8")
    except (OSError, URLError) as exc:
        raise RuntimeError(f"FRED unavailable for {series_id}") from exc

    rows: list[tuple[str, float]] = []
    for row in csv.DictReader(io.StringIO(payload)):
        value = row.get(series_id)
        if value in {None, "", "."}:
            continue
        rows.append((row["observation_date"], float(value)))
    if len(rows) < 12:
        raise RuntimeError(f"FRED returned insufficient history for {series_id}")
    return rows


def _try_load_fred_series() -> tuple[dict[str, list[tuple[str, float]]], list[str]]:
    fred = {}
    missing = []
    for series_id in FRED_SERIES:
        try:
            fred[series_id] = _load_fred_series(series_id)
        except Exception:
            missing.append(series_id)
    return fred, missing


def _pct_change(series: list[tuple[str, float]], periods: int) -> float:
    if len(series) <= periods:
        return 0.0
    old = series[-periods - 1][1]
    new = series[-1][1]
    return (new - old) / old if old else 0.0


def _diff(series: list[tuple[str, float]], periods: int) -> float:
    if len(series) <= periods:
        return 0.0
    return series[-1][1] - series[-periods - 1][1]


def _yoy(series: list[tuple[str, float]], offset: int = 0) -> float:
    end = len(series) - 1 - offset
    start = end - 12
    if start < 0:
        return 0.0
    old = series[start][1]
    new = series[end][1]
    return (new - old) / old if old else 0.0


def _cum_return(values: list[float], window: int) -> float:
    sample = values[-window:] if len(values) >= window else values
    total = 1.0
    for value in sample:
        total *= 1 + value
    return total - 1


def _direction(value: float, threshold: float = 0.0) -> str:
    return "Rising" if value >= threshold else "Falling"


def _business_cycle(growth_level: float, growth_score: float) -> str:
    above_trend = growth_level >= 0
    accelerating = growth_score >= 0
    if not above_trend and accelerating:
        return "Recovery"
    if above_trend and accelerating:
        return "Expansion"
    if above_trend and not accelerating:
        return "Slowdown"
    return "Contraction"


def _quadrant(growth_score: float, inflation_score: float) -> str:
    growth = _direction(growth_score)
    inflation = _direction(inflation_score)
    return f"{growth} growth + {inflation.lower()} inflation"


def _risk_tone(quadrant: str) -> str:
    if quadrant == "Rising growth + falling inflation":
        return "Risk-on"
    if quadrant == "Rising growth + rising inflation":
        return "Inflationary expansion"
    if quadrant == "Falling growth + rising inflation":
        return "Stagflation risk"
    return "Defensive slowdown"


def _guidance(quadrant: str) -> list[dict[str, str]]:
    if quadrant == "Rising growth + falling inflation":
        return [
            {"sleeve": "Momentum / Trend", "tilt": "Prefer", "reason": "Growth is improving while inflation pressure is easing."},
            {"sleeve": "Credit / Cyclical", "tilt": "Prefer", "reason": "Risk appetite and credit conditions are usually more supportive."},
            {"sleeve": "Defensive / Low Vol", "tilt": "Neutral", "reason": "Useful for balance, but not the primary regime beneficiary."},
        ]
    if quadrant == "Rising growth + rising inflation":
        return [
            {"sleeve": "Value / Commodity-sensitive", "tilt": "Prefer", "reason": "Nominal growth and inflation proxies are both firming."},
            {"sleeve": "Long Duration / Growth", "tilt": "Reduce", "reason": "Rising inflation can pressure duration-sensitive equities."},
            {"sleeve": "Momentum", "tilt": "Neutral", "reason": "Can work, but monitor reversal risk when rates move."},
        ]
    if quadrant == "Falling growth + rising inflation":
        return [
            {"sleeve": "Low Vol / Quality", "tilt": "Prefer", "reason": "Weakening growth with inflation pressure argues for defensive exposure."},
            {"sleeve": "Credit Carry", "tilt": "Reduce", "reason": "Falling growth can widen credit risk even if carry looks attractive."},
            {"sleeve": "High Beta Momentum", "tilt": "Reduce", "reason": "Crowded growth and beta can draw down quickly in stagflation risk."},
        ]
    return [
        {"sleeve": "Rates / Defensive", "tilt": "Prefer", "reason": "Falling inflation can support duration while growth slows."},
        {"sleeve": "Cyclical / Credit", "tilt": "Reduce", "reason": "Growth weakness can hurt cyclical earnings and spread-sensitive assets."},
        {"sleeve": "Reversal", "tilt": "Neutral", "reason": "Mean reversion can work, but needs tight drawdown controls."},
    ]


def _warnings(quadrant: str, stress_score: float) -> list[str]:
    warnings = []
    if quadrant == "Falling growth + rising inflation":
        warnings.append("Growth is weakening while inflation pressure is firm; avoid adding broad beta without a hedge.")
    if "Falling growth" in quadrant:
        warnings.append("Review credit-sensitive and cyclical stock sleeves for drawdown risk.")
    if "rising inflation" in quadrant:
        warnings.append("Monitor rates beta and long-duration growth exposure.")
    if stress_score > 0:
        warnings.append("Credit or volatility stress is rising; tighten risk limits before increasing allocation.")
    return warnings or ["No major macro-regime conflict detected; continue monitoring factor concentration."]


def _fred_regime(market_data) -> dict[str, object]:
    fred, missing = _try_load_fred_series()
    if not fred:
        raise RuntimeError("No FRED series available")

    factors = market_data.factor_returns
    equity_proxy = _cum_return(factors.get("Market beta", []), 63)
    size_proxy = _cum_return(factors.get("Size beta", []), 63)
    commodity_proxy = _cum_return(market_data.factor_returns.get("Commodity beta", []), 63)
    rates_proxy = _cum_return(factors.get("Rates beta", []), 63)
    credit_proxy = _cum_return(factors.get("Credit beta", []), 63)
    volatility_proxy = _cum_return(factors.get("Volatility beta", []), 63)

    indpro_component = _pct_change(fred["INDPRO"], 6) if "INDPRO" in fred else equity_proxy
    payroll_component = _pct_change(fred["PAYEMS"], 6) if "PAYEMS" in fred else size_proxy
    unemployment_component = -_diff(fred["UNRATE"], 6) / 10 if "UNRATE" in fred else 0.0
    growth_score = indpro_component + payroll_component + unemployment_component

    growth_level_parts = []
    if "INDPRO" in fred:
        growth_level_parts.append(_yoy(fred["INDPRO"]))
    if "PAYEMS" in fred:
        growth_level_parts.append(_yoy(fred["PAYEMS"]))
    if "UNRATE" in fred:
        growth_level_parts.append(-fred["UNRATE"][-1][1] / 100)
    growth_level = sum(growth_level_parts) / len(growth_level_parts) if growth_level_parts else _cum_return(factors.get("Market beta", []), 126)

    cpi_component = (_yoy(fred["CPIAUCSL"]) - _yoy(fred["CPIAUCSL"], 6)) if "CPIAUCSL" in fred else 0.0
    breakeven_component = _diff(fred["T10YIE"], 126) / 100 if "T10YIE" in fred else -rates_proxy
    inflation_score = cpi_component + breakeven_component + commodity_proxy

    credit_component = _diff(fred["BAA10YM"], 63) / 100 if "BAA10YM" in fred else credit_proxy
    volatility_component = _diff(fred["VIXCLS"], 63) / 100 if "VIXCLS" in fred else volatility_proxy
    stress_score = credit_component + volatility_component
    quadrant = _quadrant(growth_score, inflation_score)

    indicators = [
    ]
    if "INDPRO" in fred:
        indicators.append({"name": "Industrial production 6m", "value": f"{_pct_change(fred['INDPRO'], 6) * 100:.2f}%", "signal": "growth"})
    else:
        indicators.append({"name": "Equity proxy 3m", "value": f"{equity_proxy * 100:.2f}%", "signal": "growth"})
    if "PAYEMS" in fred:
        indicators.append({"name": "Payrolls 6m", "value": f"{_pct_change(fred['PAYEMS'], 6) * 100:.2f}%", "signal": "growth"})
    else:
        indicators.append({"name": "Size proxy 3m", "value": f"{size_proxy * 100:.2f}%", "signal": "growth"})
    if "UNRATE" in fred:
        indicators.append({"name": "Unemployment 6m change", "value": f"{_diff(fred['UNRATE'], 6):.2f} pts", "signal": "growth"})
    if "CPIAUCSL" in fred:
        indicators.append({"name": "CPI YoY", "value": f"{_yoy(fred['CPIAUCSL']) * 100:.2f}%", "signal": "inflation"})
    if "T10YIE" in fred:
        indicators.append({"name": "10Y breakeven change", "value": f"{_diff(fred['T10YIE'], 126):.2f} pts", "signal": "inflation"})
    else:
        indicators.append({"name": "Rates proxy 3m", "value": f"{rates_proxy * 100:.2f}%", "signal": "inflation"})
    indicators.append({"name": "Commodity proxy 3m", "value": f"{commodity_proxy * 100:.2f}%", "signal": "inflation"})
    if "BAA10YM" in fred:
        indicators.append({"name": "Baa spread 3m change", "value": f"{_diff(fred['BAA10YM'], 63):.2f} pts", "signal": "stress"})
    else:
        indicators.append({"name": "Credit proxy 3m", "value": f"{credit_proxy * 100:.2f}%", "signal": "stress"})
    if "VIXCLS" in fred:
        indicators.append({"name": "VIX 3m change", "value": f"{_diff(fred['VIXCLS'], 63):.2f} pts", "signal": "stress"})
    else:
        indicators.append({"name": "Volatility proxy 3m", "value": f"{volatility_proxy * 100:.2f}%", "signal": "stress"})

    source = "FRED + Yahoo ETF proxy" if not missing else "Partial FRED + Yahoo ETF proxy"
    payload = _regime_payload(source, quadrant, growth_score, inflation_score, stress_score, growth_level, indicators)
    if missing:
        payload["fallbackReason"] = "Missing FRED series: " + ", ".join(missing)
    return payload


def _proxy_regime(market_data) -> dict[str, object]:
    factors = market_data.factor_returns
    growth_score = _cum_return(factors.get("Market beta", []), 63) + _cum_return(factors.get("Size beta", []), 63)
    inflation_score = _cum_return(factors.get("Commodity beta", []), 63) - _cum_return(factors.get("Rates beta", []), 63)
    stress_score = _cum_return(factors.get("Volatility beta", []), 63) + _cum_return(factors.get("Credit beta", []), 63)
    growth_level = _cum_return(factors.get("Market beta", []), 126)
    quadrant = _quadrant(growth_score, inflation_score)
    indicators = [
        {"name": "Equity proxy 3m", "value": f"{_cum_return(factors.get('Market beta', []), 63) * 100:.2f}%", "signal": "growth"},
        {"name": "Size proxy 3m", "value": f"{_cum_return(factors.get('Size beta', []), 63) * 100:.2f}%", "signal": "growth"},
        {"name": "Commodity proxy 3m", "value": f"{_cum_return(factors.get('Commodity beta', []), 63) * 100:.2f}%", "signal": "inflation"},
        {"name": "Rates proxy 3m", "value": f"{_cum_return(factors.get('Rates beta', []), 63) * 100:.2f}%", "signal": "inflation"},
        {"name": "Volatility proxy 3m", "value": f"{_cum_return(factors.get('Volatility beta', []), 63) * 100:.2f}%", "signal": "stress"},
        {"name": "Credit proxy 3m", "value": f"{_cum_return(factors.get('Credit beta', []), 63) * 100:.2f}%", "signal": "stress"},
    ]
    return _regime_payload("Yahoo ETF proxy fallback", quadrant, growth_score, inflation_score, stress_score, growth_level, indicators)


def _regime_payload(
    source: str,
    quadrant: str,
    growth_score: float,
    inflation_score: float,
    stress_score: float,
    growth_level: float,
    indicators: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "source": source,
        "quadrant": quadrant,
        "businessCycle": _business_cycle(growth_level, growth_score),
        "riskTone": _risk_tone(quadrant),
        "growth": {"direction": _direction(growth_score), "score": round(growth_score, 4)},
        "inflation": {"direction": _direction(inflation_score), "score": round(inflation_score, 4)},
        "stress": {"direction": "Rising" if stress_score > 0 else "Falling", "score": round(stress_score, 4)},
        "indicators": indicators,
        "guidance": _guidance(quadrant),
        "warnings": _warnings(quadrant, stress_score),
    }


def build_macro_regime(market_data) -> dict[str, object]:
    try:
        return _fred_regime(market_data)
    except Exception as exc:
        payload = _proxy_regime(market_data)
        payload["fallbackReason"] = str(exc)
        return payload
