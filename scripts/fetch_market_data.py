"""Market data loading utilities.

The loader tries Yahoo Finance first when `yfinance` is installed and network
access works. If that fails, it falls back to deterministic synthetic data so
the dashboard remains runnable offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


# Current S&P 100-style universe. This is intentionally still not a
# point-in-time universe; it is a broader open-data prototype universe.
LARGE_CAP_UNIVERSE = [
    "AAPL", "ABBV", "ABT", "ACN", "ADBE", "AMAT", "AMD", "AMGN", "AMT", "AMZN",
    "AVGO", "AXP", "BA", "BAC", "BKNG", "BLK", "BMY", "BNY", "BRK-B", "C",
    "CAT", "CL", "CMCSA", "COF", "COP", "COST", "CRM", "CSCO", "CVS", "CVX",
    "DE", "DHR", "DIS", "DUK", "EMR", "FDX", "GD", "GE", "GEV", "GILD",
    "GM", "GOOG", "GOOGL", "GS", "HD", "HON", "IBM", "INTC", "INTU", "ISRG",
    "JNJ", "JPM", "KO", "LIN", "LLY", "LMT", "LOW", "LRCX", "MA", "MCD",
    "MDLZ", "MDT", "META", "MMM", "MO", "MRK", "MS", "MSFT", "MU", "NEE",
    "NFLX", "NKE", "NOW", "NVDA", "ORCL", "PEP", "PFE", "PG", "PLTR", "PM",
    "QCOM", "RTX", "SBUX", "SCHW", "SO", "SPG", "T", "TMO", "TMUS", "TSLA",
    "TXN", "UBER", "UNH", "UNP", "UPS", "USB", "V", "VZ", "WFC", "WMT",
    "XOM",
]


ETF_PROXIES = [
    "SPY", "QQQ", "IWM", "TLT", "HYG", "LQD", "GLD", "DBC", "UUP",
]


RISK_PROXIES = [
    {"ticker": "SPY", "factor": "Market beta", "purpose": "Broad U.S. equity benchmark", "use": "Compare stock strategy returns against market beta"},
    {"ticker": "QQQ", "factor": "Growth / tech", "purpose": "Nasdaq growth proxy", "use": "Separate alpha from growth crowding"},
    {"ticker": "IWM", "factor": "Small cap", "purpose": "Size and domestic cyclicality proxy", "use": "Detect small-cap sensitivity"},
    {"ticker": "TLT", "factor": "Rates duration", "purpose": "Long-duration Treasury proxy", "use": "Map rate-sensitive growth exposure"},
    {"ticker": "HYG", "factor": "Credit spread", "purpose": "High-yield credit proxy", "use": "Stress-test credit-sensitive equities"},
    {"ticker": "LQD", "factor": "Investment grade credit", "purpose": "IG credit proxy", "use": "Benchmark spread-risk beta"},
    {"ticker": "GLD", "factor": "Gold / real asset", "purpose": "Inflation hedge proxy", "use": "Compare inflation sleeve behavior"},
    {"ticker": "DBC", "factor": "Commodities", "purpose": "Broad commodity proxy", "use": "Monitor commodity/inflation linkage"},
    {"ticker": "UUP", "factor": "Dollar FX", "purpose": "USD strength proxy", "use": "Explain multinational revenue exposure"},
]


@dataclass(frozen=True)
class MarketData:
    dates: list[str]
    stock_close: dict[str, list[float]]
    stock_high: dict[str, list[float]]
    stock_low: dict[str, list[float]]
    stock_volume: dict[str, list[float]]
    stock_returns: dict[str, list[float]]
    factor_returns: dict[str, list[float]]
    source: str


def _synthetic_return(day: int, idx: int, base: float = 0.00012) -> float:
    cycle = ((day * (idx + 5)) % 19 - 9) / 10_000
    seasonal = ((idx % 7) - 3) / 60_000
    shock = -0.002 if day in (7, 16) and idx % 6 in (0, 1) else 0.0
    return base + cycle + seasonal + shock


def _load_synthetic_market_data(days: int = 20) -> MarketData:
    """Return deterministic stock and factor returns for the dashboard.

    Output format intentionally mirrors what a real loader should return:
    date-indexed return series keyed by ticker/factor name.
    """
    end_date = date(2026, 6, 9)
    dates = []
    cursor = end_date
    while len(dates) < days:
        if cursor.weekday() < 5:
            dates.append(cursor.isoformat())
        cursor -= timedelta(days=1)
    dates.reverse()
    stock_returns = {
        ticker: [_synthetic_return(day, idx) for day in range(days)]
        for idx, ticker in enumerate(LARGE_CAP_UNIVERSE)
    }
    stock_close = {}
    stock_high = {}
    stock_low = {}
    stock_volume = {}
    for idx, ticker in enumerate(LARGE_CAP_UNIVERSE):
        price = 100.0 + idx
        closes = []
        highs = []
        lows = []
        volumes = []
        for day, ret in enumerate(stock_returns[ticker]):
            price *= 1 + ret
            daily_range = 0.006 + ((day + idx) % 7) / 1000
            closes.append(price)
            highs.append(price * (1 + daily_range))
            lows.append(price * (1 - daily_range))
            volumes.append(1_000_000 + idx * 20_000 + ((day * (idx + 3)) % 11) * 35_000)
        stock_close[ticker] = closes
        stock_high[ticker] = highs
        stock_low[ticker] = lows
        stock_volume[ticker] = volumes
    factor_returns = {
        "Market beta": [_synthetic_return(day, 1, 0.00010) for day in range(days)],
        "Size beta": [_synthetic_return(day, 2, 0.00003) for day in range(days)],
        "Value beta": [_synthetic_return(day, 3, 0.00002) for day in range(days)],
        "Momentum beta": [_synthetic_return(day, 4, 0.00008) for day in range(days)],
        "Rates beta": [_synthetic_return(day, 5, -0.00001) for day in range(days)],
        "Credit beta": [_synthetic_return(day, 6, 0.00004) for day in range(days)],
        "Volatility beta": [_synthetic_return(day, 7, -0.00002) for day in range(days)],
        "USD beta": [_synthetic_return(day, 8, 0.00001) for day in range(days)],
        "Commodity beta": [_synthetic_return(day, 9, 0.00004) for day in range(days)],
    }
    return MarketData(
        dates=dates,
        stock_close=stock_close,
        stock_high=stock_high,
        stock_low=stock_low,
        stock_volume=stock_volume,
        stock_returns=stock_returns,
        factor_returns=factor_returns,
        source="synthetic",
    )


def _load_yahoo_market_data(days: int = 1260) -> MarketData:
    """Load stock and ETF proxy returns from Yahoo Finance via yfinance."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("yfinance is not installed") from exc

    tickers = LARGE_CAP_UNIVERSE + ETF_PROXIES
    raw = yf.download(
        tickers=tickers,
        period="10y",
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )
    if raw.empty:
        raise RuntimeError("Yahoo Finance returned an empty dataset")

    if "Close" in raw:
        prices = raw["Close"]
    else:
        raise RuntimeError("Yahoo Finance response did not contain close prices")

    high = raw["High"] if "High" in raw else prices
    low = raw["Low"] if "Low" in raw else prices
    volume = raw["Volume"] if "Volume" in raw else prices * 0 + 1

    prices = prices.dropna(axis=1, how="all").ffill().dropna(how="all")
    high = high.reindex(prices.index).reindex(columns=prices.columns).ffill()
    low = low.reindex(prices.index).reindex(columns=prices.columns).ffill()
    volume = volume.reindex(prices.index).reindex(columns=prices.columns).fillna(0)
    returns = prices.pct_change().dropna(how="all").tail(days)
    if returns.empty:
        raise RuntimeError("Yahoo Finance return series is empty after cleaning")

    available = set(returns.columns.astype(str))
    missing_stocks = [ticker for ticker in LARGE_CAP_UNIVERSE if ticker not in available]
    missing_proxies = [ticker for ticker in ETF_PROXIES if ticker not in available]
    if len(missing_stocks) > len(LARGE_CAP_UNIVERSE) // 2 or missing_proxies:
        raise RuntimeError("Yahoo Finance data coverage is insufficient for this prototype")

    clean_returns = returns.fillna(0.0)
    clean_prices = prices.reindex(clean_returns.index).ffill()
    clean_high = high.reindex(clean_returns.index).fillna(clean_prices)
    clean_low = low.reindex(clean_returns.index).fillna(clean_prices)
    clean_volume = volume.reindex(clean_returns.index).fillna(0.0)
    dates = [str(idx.date()) for idx in clean_returns.index]
    stock_returns = {
        ticker: [float(value) for value in clean_returns[ticker].tolist()]
        for ticker in LARGE_CAP_UNIVERSE
        if ticker in clean_returns
    }
    stock_close = {
        ticker: [float(value) for value in clean_prices[ticker].tolist()]
        for ticker in stock_returns
    }
    stock_high = {
        ticker: [float(value) for value in clean_high[ticker].tolist()]
        for ticker in stock_returns
    }
    stock_low = {
        ticker: [float(value) for value in clean_low[ticker].tolist()]
        for ticker in stock_returns
    }
    stock_volume = {
        ticker: [float(value) for value in clean_volume[ticker].tolist()]
        for ticker in stock_returns
    }

    def series(ticker: str) -> list[float]:
        return [float(value) for value in clean_returns[ticker].tolist()]

    def spread(long_ticker: str, short_ticker: str) -> list[float]:
        long_series = series(long_ticker)
        short_series = series(short_ticker)
        return [a - b for a, b in zip(long_series, short_series)]

    factor_returns = {
        "Market beta": series("SPY"),
        "Size beta": spread("IWM", "SPY"),
        "Value beta": spread("IWD", "IWF") if {"IWD", "IWF"}.issubset(available) else spread("SPY", "QQQ"),
        "Momentum beta": spread("QQQ", "SPY"),
        "Rates beta": series("TLT"),
        "Credit beta": spread("HYG", "LQD"),
        "Volatility beta": [-ret for ret in series("SPY")],
        "USD beta": series("UUP"),
        "Commodity beta": series("DBC"),
    }
    return MarketData(
        dates=dates,
        stock_close=stock_close,
        stock_high=stock_high,
        stock_low=stock_low,
        stock_volume=stock_volume,
        stock_returns=stock_returns,
        factor_returns=factor_returns,
        source="yahoo",
    )


def load_market_data(days: int = 1260, source: str = "auto") -> MarketData:
    """Load market data.

    Args:
        days: Number of daily return observations to keep.
        source: `auto`, `yahoo`, or `synthetic`.
    """
    if source == "synthetic":
        return _load_synthetic_market_data(days)
    if source in {"auto", "yahoo"}:
        try:
            return _load_yahoo_market_data(days)
        except Exception as exc:
            if source == "yahoo":
                raise
            print(f"Yahoo Finance unavailable; using synthetic data instead. Reason: {exc}")
    return _load_synthetic_market_data(days)


def load_market_news() -> list[dict[str, str]]:
    """Placeholder news feed. Replace with approved news API output later."""
    return [
        {
            "time": "10:21 AM",
            "source": "News API placeholder",
            "headline": "Semiconductor leadership remains concentrated; watch overlap across momentum and quality books.",
            "tickers": "NVDA, AVGO, AMD",
            "impact": "High",
        },
        {
            "time": "10:14 AM",
            "source": "Macro feed placeholder",
            "headline": "Rates drift lower before inflation release; duration-sensitive growth exposure should be reviewed.",
            "tickers": "ADBE, SNOW, DDOG",
            "impact": "Medium",
        },
        {
            "time": "09:58 AM",
            "source": "News sentiment placeholder",
            "headline": "Airlines and consumer cyclicals trade weaker on credit-spread concerns.",
            "tickers": "DAL, AAL, CCL",
            "impact": "High",
        },
        {
            "time": "09:43 AM",
            "source": "Broker feed placeholder",
            "headline": "Mega-cap earnings revisions remain positive but correlation among winners is rising.",
            "tickers": "MSFT, META, AMZN",
            "impact": "Medium",
        },
    ]
