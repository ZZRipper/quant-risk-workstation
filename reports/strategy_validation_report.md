# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-08-09 to 2022-08-03 / 2022-08-04 to 2026-08-06

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.36 | 0.80 | 0.44 | -53.11% | -26.73% | 52.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.89 | 1.36 | 0.48 | -36.11% | -21.58% | 55.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.14 | 1.03 | 0.89 | -38.12% | -21.28% | 53.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.38 | 0.48 | 0.86 | -65.31% | -23.57% | 51.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.89 | 1.10 | 0.20 | -28.10% | -20.33% | 52.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.89 | 1.05 | 0.16 | -32.49% | -22.96% | 52.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.55 | 0.98 | 0.43 | -35.34% | -19.38% | 53.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.66 | 0.98 | 0.31 | -44.45% | -22.44% | 55.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.20 | 0.02 | 0.21 | -43.87% | -17.89% | 51.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.19 | 0.82 | 0.63 | -52.72% | -29.93% | 53.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.65 | 1.16 | 0.51 | -31.20% | -23.79% | 51.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.26 | 0.92 | 0.66 | -57.22% | -27.40% | 53.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.50 | 1.26 | 0.75 | -31.69% | -20.97% | 53.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.67 | 1.38 | 0.71 | -27.62% | -18.07% | 52.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.78 | 0.98 | 0.20 | -32.54% | -17.86% | 51.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.38 | 0.92 | 0.54 | -33.14% | -25.25% | 50.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.59 | 1.20 | 0.61 | -27.56% | -19.39% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.69 | 0.85 | 0.16 | -39.67% | -20.85% | 53.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.11 | 0.98 | -0.13 | -30.79% | -16.06% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.08 | 0.25 | 0.17 | -48.24% | -35.75% | 52.7% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
