# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-11-29 to 2022-11-22 / 2022-11-23 to 2026-11-25

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.33 | 0.95 | 0.62 | -53.11% | -23.91% | 53.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.71 | 1.22 | 0.51 | -36.11% | -34.42% | 55.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.13 | 0.71 | 0.58 | -38.13% | -36.63% | 52.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.41 | 0.29 | 0.71 | -66.86% | -28.83% | 51.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.75 | 1.02 | 0.27 | -28.39% | -27.27% | 52.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.69 | 1.04 | 0.35 | -32.49% | -25.66% | 52.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.52 | 0.90 | 0.37 | -35.34% | -17.36% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.56 | 0.97 | 0.41 | -44.45% | -18.31% | 55.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.18 | -0.36 | -0.18 | -44.50% | -32.32% | 50.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.05 | 0.92 | 0.87 | -52.72% | -17.30% | 53.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.58 | 1.03 | 0.45 | -33.92% | -27.29% | 51.1% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.19 | 1.04 | 0.86 | -57.22% | -19.16% | 53.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.43 | 1.15 | 0.72 | -31.69% | -26.08% | 52.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.52 | 1.35 | 0.83 | -27.62% | -19.28% | 52.0% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.66 | 1.01 | 0.35 | -34.55% | -17.86% | 51.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.27 | 0.78 | 0.51 | -33.71% | -32.54% | 50.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.48 | 1.09 | 0.61 | -27.56% | -26.68% | 52.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.61 | 0.63 | 0.02 | -39.67% | -24.18% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.93 | 0.97 | 0.04 | -30.79% | -19.68% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
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
