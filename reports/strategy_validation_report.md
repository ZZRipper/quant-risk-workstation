# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: Partial FRED + Yahoo ETF proxy
- Fallback note: Missing FRED series: T10YIE, DGS10, BAA10YM, VIXCLS

## Validation Table

| ID | Strategy | Latest Top Holdings | Signal | Data | Sharpe | Max DD | Hit Rate | Avg Cost bps/day | Macro Fit | Status | Reason |
|---|---|---|---|---|---:|---:|---:|---:|---|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | ORCL, QCOM, ADBE, NOW, CRM, META, IBM, MSFT, INTU, AVGO | Short-term reversal = negative trailing 5-day return. | Close-to-close returns | 0.46 | -35.78% | 51.2% | 4.254 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-02 | WQ Alpha 004 - Rank Momentum | INTC, AMD, MU, LRCX, QCOM, AMAT, TXN, CSCO, UNH, CVS | Rank momentum = trailing 60-day cumulative return. | Close-to-close returns | 1.25 | -28.88% | 55.6% | 1.632 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | AMAT, LRCX, SBUX, CVS, INTC, GD, TMUS, LMT, KO, SPG | Volume-price divergence = trailing 5-day return multiplied by 20-day volume ratio. | Close-to-close returns, volume | 0.82 | -33.19% | 54.0% | 5.136 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | LRCX, MU, AMAT, INTC, AMD, BA, HON, QCOM, TXN, GEV | Open-close pressure proxy = latest return minus trailing 20-day average return. | Close-to-close returns | 0.16 | -47.48% | 52.2% | 6.636 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-05 | WQ Alpha 021 - Trend Stability | MU, AMD, INTC, CSCO, QCOM, AMAT, CVS, TXN, LRCX, UNH | Trend stability = trailing 40-day return minus volatility penalty. | Close-to-close returns | 1.02 | -28.39% | 52.9% | 1.905 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | MU, AMD, INTC, QCOM, ORCL, CSCO, TXN, LRCX, AMAT, UNH | Delayed momentum = 40-day cumulative return, lagged by 5 days. | Close-to-close returns | 0.91 | -31.11% | 52.3% | 1.724 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | INTU, CMCSA, SCHW, WMT, TSLA, NEE, GEV, GOOGL, JNJ, ISRG | Correlation reversal = negative 20-day return-volume correlation. | Close-to-close returns, volume | 0.56 | -27.80% | 52.0% | 1.691 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | INTU, ADBE, ORCL, AVGO, GEV, CRM, QCOM, MSFT, AMZN, META | VWAP-style mean reversion = negative deviation from 20-day average close. | Close prices | 0.73 | -30.26% | 53.1% | 3.383 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-09 | WQ Alpha 041 - High-Low Range | NOW, NEE, CL, PG, PEP, SCHW, LIN, ABBV, CMCSA, MDT | High-low range = negative current range relative to trailing average range. | High, low, close | -0.23 | -31.85% | 51.0% | 6.810 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | ORCL, ADBE, AVGO, GEV, LMT, META, GS, GILD, NKE, HD | Volume acceleration = recent return times short-volume ratio minus long-volume ratio. | Close-to-close returns, volume | 0.46 | -44.05% | 52.4% | 3.956 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-11 | WQ Alpha 051 - Decay Momentum | AMAT, MU, LRCX, LLY, C, GE, CVS, BAC, WFC, IBM | Decay momentum = recency-weighted 20-day return. | Close-to-close returns | 0.96 | -33.92% | 52.5% | 2.899 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | ORCL, ADBE, QCOM, CRM, MSFT, NOW, META, GEV, AVGO, INTU | Turnover reversal = negative recent return times 20-day volume ratio. | Close-to-close returns, volume | 0.46 | -39.94% | 51.5% | 4.172 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | AMAT, LRCX, C, MU, BAC, CVS, WFC, MDT, USB, AMGN | Price-volume rank = 10-day return plus volume-ratio participation adjustment. | Close-to-close returns, volume | 1.04 | -31.24% | 53.5% | 3.958 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-14 | WQ Alpha 071 - Composite Rank | MU, QCOM, AMD, CSCO, ORCL, LLY, IBM, LRCX, NOW, AMAT | Composite rank = 30-day trend minus 5-day reversal pressure and volatility penalty. | Close-to-close returns | 1.17 | -21.70% | 52.4% | 2.579 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-15 | WQ Alpha 078 - Correlation Break | SCHW, TMO, MU, AMD, GOOGL, BAC, FDX, BLK, INTC, ACN | Correlation break = absolute difference between 10-day and 40-day return-volume correlation. | Close-to-close returns, volume | 0.51 | -34.55% | 50.4% | 3.153 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-16 | WQ Alpha 083 - Range Momentum | MU, AMAT, LRCX, UPS, IBM, LLY, FDX, GD, GE, AMGN | Range momentum = 15-day return multiplied by range expansion. | Close-to-close returns, high, low, close | 0.79 | -33.71% | 50.2% | 4.741 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | MU, AMD, QCOM, CSCO, LLY, IBM, AMAT, LRCX, NOW, GE | Liquidity-adjusted momentum = 30-day momentum divided by volume ratio. | Close-to-close returns, volume | 1.13 | -21.64% | 52.7% | 3.131 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | INTU, GEV, CMCSA, LOW, SBUX, T, NEE, WMT, PEP, UBER | Delayed reversal = negative 20-day return, lagged by 5 days. | Close-to-close returns | 0.56 | -33.19% | 52.7% | 2.487 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | AMD, INTC, MS, BNY, CSCO, UNH, CVS, MU, C, TXN | Risk-controlled momentum = 60-day momentum divided by trailing volatility. | Close-to-close returns | 0.93 | -22.56% | 54.2% | 1.693 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | ORCL, ADBE, COP, NOW, XOM, INTU, CRM, MO, CVX, MSFT | Close-to-open reversal proxy = negative latest return. | Close-to-close returns | -0.12 | -58.76% | 51.7% | 5.401 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
