# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-10-21 to 2022-10-14 / 2022-10-17 to 2026-10-19

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.29 | 1.08 | 0.80 | -53.11% | -23.91% | 53.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.65 | 1.48 | 0.83 | -36.11% | -26.25% | 56.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.08 | 1.03 | 0.95 | -38.13% | -29.11% | 53.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.48 | 0.66 | 1.14 | -66.86% | -23.57% | 51.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.69 | 1.17 | 0.49 | -28.39% | -21.08% | 52.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.62 | 1.21 | 0.58 | -32.49% | -22.96% | 53.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.42 | 1.23 | 0.81 | -35.34% | -17.36% | 54.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.51 | 1.21 | 0.70 | -44.45% | -18.31% | 56.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.28 | 0.07 | 0.35 | -44.50% | -23.59% | 51.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.01 | 1.09 | 1.07 | -52.72% | -17.30% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.54 | 1.25 | 0.72 | -33.92% | -23.79% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.13 | 1.21 | 1.08 | -57.22% | -19.16% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.39 | 1.50 | 1.12 | -31.69% | -20.97% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.50 | 1.46 | 0.96 | -27.62% | -18.07% | 52.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.61 | 1.20 | 0.59 | -34.55% | -17.86% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.24 | 0.93 | 0.69 | -33.71% | -31.73% | 50.1% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.45 | 1.27 | 0.82 | -27.56% | -20.62% | 52.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.52 | 1.02 | 0.50 | -39.67% | -17.62% | 53.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.85 | 1.15 | 0.29 | -30.79% | -19.68% | 54.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.09 | 0.49 | 0.59 | -53.80% | -22.48% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
