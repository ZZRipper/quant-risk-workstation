# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-07-12 to 2022-07-06 / 2022-07-07 to 2026-07-09

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.30 | 0.78 | 0.48 | -53.11% | -26.73% | 51.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.88 | 1.49 | 0.61 | -36.11% | -19.66% | 55.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.09 | 1.17 | 1.08 | -38.13% | -20.77% | 54.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.46 | 0.61 | 1.07 | -65.31% | -23.57% | 52.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.89 | 1.17 | 0.28 | -28.10% | -20.33% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.85 | 1.22 | 0.37 | -32.49% | -22.96% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.49 | 0.98 | 0.50 | -35.34% | -19.38% | 53.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.60 | 1.04 | 0.44 | -44.45% | -22.44% | 55.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.27 | 0.09 | 0.36 | -43.87% | -16.60% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.13 | 0.88 | 0.75 | -52.72% | -29.93% | 53.7% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.61 | 1.24 | 0.62 | -30.18% | -23.79% | 52.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.19 | 0.89 | 0.70 | -57.22% | -27.40% | 52.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.46 | 1.32 | 0.86 | -31.69% | -20.97% | 53.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.61 | 1.44 | 0.83 | -27.62% | -18.07% | 52.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.71 | 0.98 | 0.27 | -32.54% | -17.86% | 51.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.35 | 1.05 | 0.71 | -33.14% | -25.25% | 50.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.54 | 1.30 | 0.76 | -27.56% | -19.39% | 52.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.59 | 1.03 | 0.44 | -39.67% | -20.85% | 54.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.13 | 1.03 | -0.11 | -30.79% | -16.06% | 54.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.07 | 0.30 | 0.23 | -48.24% | -35.75% | 52.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
