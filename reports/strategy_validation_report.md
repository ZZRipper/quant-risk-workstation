# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-11-28 to 2022-11-18 / 2022-11-21 to 2026-11-23

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.34 | 0.94 | 0.60 | -53.11% | -23.91% | 53.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.70 | 1.22 | 0.51 | -36.11% | -34.42% | 55.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.13 | 0.75 | 0.61 | -38.13% | -35.08% | 52.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.40 | 0.35 | 0.76 | -66.86% | -24.82% | 51.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.75 | 1.00 | 0.26 | -28.39% | -27.27% | 52.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.67 | 1.02 | 0.35 | -32.49% | -25.66% | 52.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.52 | 0.93 | 0.41 | -35.34% | -17.36% | 53.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.56 | 1.00 | 0.43 | -44.45% | -18.31% | 55.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.19 | -0.36 | -0.17 | -44.50% | -32.32% | 50.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.04 | 0.93 | 0.88 | -52.72% | -17.30% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.58 | 1.02 | 0.44 | -33.92% | -27.29% | 51.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.18 | 1.05 | 0.87 | -57.22% | -19.16% | 53.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.44 | 1.14 | 0.71 | -31.69% | -26.08% | 52.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.51 | 1.33 | 0.82 | -27.62% | -19.28% | 51.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.66 | 0.97 | 0.31 | -34.55% | -17.86% | 51.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.28 | 0.78 | 0.50 | -33.71% | -32.54% | 49.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.47 | 1.08 | 0.61 | -27.56% | -26.68% | 51.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.61 | 0.69 | 0.08 | -39.67% | -24.18% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.92 | 0.96 | 0.04 | -30.79% | -19.68% | 54.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.03 | 0.30 | 0.33 | -53.80% | -28.01% | 52.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
