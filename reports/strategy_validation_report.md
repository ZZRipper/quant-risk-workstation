# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-11-04 to 2022-10-28 / 2022-10-31 to 2026-11-02

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.33 | 0.99 | 0.66 | -53.11% | -23.91% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.71 | 1.33 | 0.62 | -36.11% | -26.38% | 55.7% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.16 | 0.87 | 0.71 | -38.13% | -29.65% | 53.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.43 | 0.55 | 0.97 | -66.86% | -23.57% | 51.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.76 | 1.05 | 0.29 | -28.39% | -21.81% | 52.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.69 | 1.09 | 0.40 | -32.49% | -22.96% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.51 | 1.08 | 0.57 | -35.34% | -17.36% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.57 | 1.08 | 0.52 | -44.45% | -18.31% | 56.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.22 | -0.15 | 0.07 | -44.50% | -27.13% | 50.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.02 | 0.93 | 0.91 | -52.72% | -17.30% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.60 | 1.15 | 0.55 | -33.92% | -23.80% | 51.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.19 | 1.10 | 0.91 | -57.22% | -19.16% | 53.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.48 | 1.35 | 0.87 | -31.69% | -20.97% | 53.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.52 | 1.43 | 0.91 | -27.62% | -18.07% | 52.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.66 | 1.12 | 0.46 | -34.55% | -17.86% | 52.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.30 | 0.86 | 0.56 | -33.71% | -31.73% | 50.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.48 | 1.17 | 0.69 | -27.56% | -20.71% | 52.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.59 | 0.79 | 0.20 | -39.67% | -17.62% | 53.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.93 | 1.04 | 0.11 | -30.79% | -19.68% | 54.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.00 | 0.27 | 0.27 | -53.80% | -22.45% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
