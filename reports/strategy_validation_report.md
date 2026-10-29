# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-11-01 to 2022-10-25 / 2022-10-26 to 2026-10-28

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.35 | 0.99 | 0.64 | -53.11% | -23.91% | 53.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.69 | 1.42 | 0.73 | -36.11% | -26.25% | 56.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.13 | 0.99 | 0.86 | -38.13% | -29.11% | 53.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.45 | 0.58 | 1.03 | -66.86% | -23.57% | 51.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.72 | 1.11 | 0.38 | -28.39% | -21.55% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.67 | 1.16 | 0.49 | -32.49% | -22.96% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.48 | 1.13 | 0.66 | -35.34% | -17.36% | 54.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.56 | 1.16 | 0.60 | -44.45% | -18.31% | 56.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.24 | -0.03 | 0.21 | -44.50% | -23.59% | 50.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.03 | 1.01 | 0.98 | -52.72% | -17.30% | 53.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.57 | 1.18 | 0.60 | -33.92% | -23.79% | 51.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.19 | 1.12 | 0.92 | -57.22% | -19.16% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.43 | 1.42 | 0.99 | -31.69% | -20.97% | 53.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.51 | 1.43 | 0.92 | -27.62% | -18.07% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.65 | 1.14 | 0.49 | -34.55% | -17.86% | 52.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.28 | 0.86 | 0.58 | -33.71% | -31.73% | 50.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.46 | 1.21 | 0.75 | -27.56% | -20.71% | 52.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.57 | 0.99 | 0.41 | -39.67% | -17.62% | 53.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.89 | 1.07 | 0.19 | -30.79% | -19.68% | 54.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.03 | 0.44 | 0.47 | -53.80% | -22.48% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
