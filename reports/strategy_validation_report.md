# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-09-13 to 2022-09-07 / 2022-09-08 to 2026-09-11

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.36 | 0.90 | 0.53 | -53.11% | -23.91% | 53.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.75 | 1.36 | 0.61 | -36.11% | -24.48% | 55.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.13 | 0.96 | 0.83 | -38.12% | -26.89% | 53.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.43 | 0.57 | 1.00 | -65.31% | -23.57% | 51.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.83 | 1.17 | 0.33 | -28.10% | -20.33% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.78 | 1.17 | 0.40 | -32.49% | -22.96% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.51 | 1.05 | 0.54 | -35.34% | -17.36% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.60 | 1.09 | 0.49 | -44.45% | -18.31% | 55.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.23 | -0.01 | 0.22 | -43.87% | -18.85% | 51.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.11 | 0.84 | 0.73 | -52.72% | -24.92% | 53.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.60 | 1.14 | 0.54 | -31.20% | -23.79% | 51.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.24 | 1.03 | 0.79 | -57.22% | -20.39% | 53.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.47 | 1.31 | 0.84 | -31.69% | -20.97% | 53.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.61 | 1.47 | 0.86 | -27.62% | -18.07% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.71 | 1.06 | 0.36 | -32.54% | -17.86% | 52.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.33 | 0.90 | 0.56 | -33.14% | -28.48% | 50.1% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.53 | 1.25 | 0.71 | -27.56% | -19.39% | 52.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.64 | 0.85 | 0.21 | -39.67% | -18.55% | 53.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.96 | 0.98 | 0.02 | -30.79% | -16.20% | 54.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.03 | 0.34 | 0.31 | -48.24% | -29.23% | 52.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
