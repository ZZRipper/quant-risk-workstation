# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-07-19 to 2022-07-12 / 2022-07-13 to 2026-07-15

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.32 | 0.76 | 0.44 | -53.11% | -26.73% | 52.1% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.88 | 1.46 | 0.57 | -36.11% | -19.66% | 55.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.06 | 1.17 | 1.10 | -38.13% | -20.77% | 53.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.47 | 0.58 | 1.05 | -65.31% | -23.57% | 52.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.89 | 1.15 | 0.26 | -28.10% | -20.33% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.83 | 1.16 | 0.33 | -32.49% | -22.96% | 52.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.49 | 0.99 | 0.50 | -35.34% | -19.38% | 53.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.60 | 1.00 | 0.39 | -44.45% | -22.44% | 55.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.27 | 0.09 | 0.36 | -43.87% | -16.77% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.11 | 0.84 | 0.72 | -52.72% | -29.93% | 53.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.57 | 1.27 | 0.70 | -30.83% | -23.79% | 52.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.20 | 0.87 | 0.67 | -57.22% | -27.40% | 53.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.42 | 1.36 | 0.94 | -31.69% | -20.97% | 53.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.59 | 1.44 | 0.84 | -27.62% | -18.07% | 52.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.73 | 0.99 | 0.26 | -32.54% | -17.86% | 51.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.30 | 1.06 | 0.76 | -33.14% | -25.25% | 50.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.50 | 1.30 | 0.80 | -27.56% | -19.39% | 52.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.58 | 1.01 | 0.43 | -39.67% | -20.85% | 54.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.13 | 1.01 | -0.12 | -30.79% | -16.06% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.06 | 0.33 | 0.26 | -48.24% | -35.73% | 52.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
