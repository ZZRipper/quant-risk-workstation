# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-06-28 to 2022-06-22 / 2022-06-23 to 2026-06-25

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.32 | 0.72 | 0.40 | -53.11% | -26.73% | 51.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.89 | 1.61 | 0.72 | -36.11% | -19.66% | 55.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.11 | 1.24 | 1.13 | -38.13% | -20.77% | 54.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.49 | 0.67 | 1.16 | -65.31% | -23.57% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.88 | 1.28 | 0.40 | -28.10% | -20.33% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.79 | 1.37 | 0.58 | -32.49% | -22.96% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.49 | 0.91 | 0.42 | -35.34% | -19.38% | 52.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.63 | 0.89 | 0.26 | -44.45% | -22.44% | 54.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.27 | 0.07 | 0.34 | -43.87% | -16.40% | 51.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.15 | 0.78 | 0.63 | -52.72% | -29.93% | 53.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.61 | 1.34 | 0.73 | -30.18% | -23.79% | 52.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.18 | 0.82 | 0.64 | -57.22% | -27.40% | 52.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.44 | 1.44 | 1.00 | -31.69% | -20.97% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.61 | 1.52 | 0.91 | -27.62% | -18.07% | 52.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.71 | 0.88 | 0.17 | -32.54% | -17.86% | 51.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.33 | 1.18 | 0.86 | -33.14% | -25.25% | 50.7% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.53 | 1.42 | 0.89 | -27.56% | -19.39% | 52.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.59 | 0.97 | 0.38 | -39.67% | -20.85% | 53.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.12 | 1.16 | 0.04 | -30.79% | -16.06% | 54.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.09 | 0.21 | 0.12 | -48.24% | -35.73% | 52.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
