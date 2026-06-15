# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: Partial FRED + Yahoo ETF proxy
- Fallback note: Missing FRED series: INDPRO, T10YIE, DGS10, BAA10YM, VIXCLS

## Validation Table

| ID | Strategy | Latest Top Holdings | Signal | Data | Sharpe | Max DD | Hit Rate | Avg Cost bps/day | Macro Fit | Status | Reason |
|---|---|---|---|---|---:|---:|---:|---:|---|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | QCOM, AVGO, MU, AMD, ORCL, IBM, CRM, NOW, TSLA, GEV | Short-term reversal = negative trailing 5-day return. | Close-to-close returns | 0.45 | -35.78% | 51.2% | 4.204 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-02 | WQ Alpha 004 - Rank Momentum | INTC, AMD, MU, QCOM, CSCO, LRCX, TXN, AMAT, UNH, ORCL | Rank momentum = trailing 60-day cumulative return. | Close-to-close returns | 1.22 | -28.88% | 55.5% | 1.619 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | USB, KO, CVS, UNH, JNJ, SPG, MMM, CL, PG, MDLZ | Volume-price divergence = trailing 5-day return multiplied by 20-day volume ratio. | Close-to-close returns, volume | 0.82 | -33.19% | 54.0% | 5.167 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | TMUS, VZ, T, PM, COP, KO, CL, MO, WMT, MDLZ | Open-close pressure proxy = latest return minus trailing 20-day average return. | Close-to-close returns | 0.16 | -47.48% | 52.2% | 6.668 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-05 | WQ Alpha 021 - Trend Stability | MU, AMD, INTC, CSCO, QCOM, UNH, CVS, TXN, AMAT, LLY | Trend stability = trailing 40-day return minus volatility penalty. | Close-to-close returns | 1.00 | -28.39% | 52.9% | 1.930 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | MU, AMD, INTC, QCOM, ORCL, TXN, CSCO, LRCX, AVGO, AMAT | Delayed momentum = 40-day cumulative return, lagged by 5 days. | Close-to-close returns | 0.88 | -31.11% | 52.3% | 1.710 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | INTU, CMCSA, SCHW, WMT, NEE, JNJ, TSLA, ISRG, GEV, CL | Correlation reversal = negative 20-day return-volume correlation. | Close-to-close returns, volume | 0.54 | -27.80% | 51.9% | 1.677 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | INTU, QCOM, GEV, AVGO, TSLA, AMZN, NVDA, HON, TXN, GILD | VWAP-style mean reversion = negative deviation from 20-day average close. | Close prices | 0.72 | -30.26% | 53.1% | 3.351 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-09 | WQ Alpha 041 - High-Low Range | NEE, ABBV, CSCO, PFE, HD, LOW, PG, PLTR, MSFT, CRM | High-low range = negative current range relative to trailing average range. | High, low, close | -0.25 | -31.85% | 50.9% | 6.776 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | AVGO, GEV, ORCL, GILD, MU, LRCX, META, AAPL, INTU, ADBE | Volume acceleration = recent return times short-volume ratio minus long-volume ratio. | Close-to-close returns, volume | 0.49 | -44.05% | 52.5% | 4.082 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-11 | WQ Alpha 051 - Decay Momentum | AMAT, LLY, MU, IBM, WFC, BAC, DHR, LRCX, AMT, SPG | Decay momentum = recency-weighted 20-day return. | Close-to-close returns | 0.96 | -33.92% | 52.6% | 2.908 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | AVGO, ORCL, QCOM, GEV, MU, AMD, TSLA, CAT, ADBE, LRCX | Turnover reversal = negative recent return times 20-day volume ratio. | Close-to-close returns, volume | 0.45 | -39.94% | 51.5% | 4.120 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | AMAT, ORCL, IBM, WFC, BAC, C, CVS, UNH, DHR, NOW | Price-volume rank = 10-day return plus volume-ratio participation adjustment. | Close-to-close returns, volume | 1.02 | -31.24% | 53.4% | 3.909 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-14 | WQ Alpha 071 - Composite Rank | MU, AMD, QCOM, CSCO, ORCL, LRCX, IBM, AMAT, INTC, NOW | Composite rank = 30-day trend minus 5-day reversal pressure and volatility penalty. | Close-to-close returns | 1.16 | -21.70% | 52.4% | 2.602 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-15 | WQ Alpha 078 - Correlation Break | SCHW, TMO, MU, AMD, INTC, GOOGL, TSLA, HD, TXN, LLY | Correlation break = absolute difference between 10-day and 40-day return-volume correlation. | Close-to-close returns, volume | 0.49 | -34.55% | 50.4% | 3.183 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-16 | WQ Alpha 083 - Range Momentum | MU, AMAT, LRCX, IBM, GM, MMM, ORCL, GE, C, AMD | Range momentum = 15-day return multiplied by range expansion. | Close-to-close returns, high, low, close | 0.79 | -33.71% | 50.2% | 4.766 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | MU, CSCO, AMD, IBM, QCOM, NOW, LLY, INTC, AMAT, LRCX | Liquidity-adjusted momentum = 30-day momentum divided by volume ratio. | Close-to-close returns, volume | 1.13 | -21.64% | 52.7% | 3.163 | Watch | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | INTU, NEE, GEV, CMCSA, WMT, ISRG, T, AMZN, SBUX, PEP | Delayed reversal = negative 20-day return, lagged by 5 days. | Close-to-close returns | 0.55 | -33.09% | 52.6% | 2.456 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | AMD, MS, UNH, BNY, CSCO, INTC, MU, CVS, C, GS | Risk-controlled momentum = 60-day momentum divided by trailing volatility. | Close-to-close returns | 0.90 | -22.56% | 54.1% | 1.687 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | QCOM, CAT, GEV, GM, AVGO, AMD, MU, HON, UPS, TSLA | Close-to-open reversal proxy = negative latest return. | Close-to-close returns | -0.12 | -58.76% | 51.7% | 5.395 | Neutral | Reject | drawdown is beyond watch threshold; average daily transaction cost is high. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
