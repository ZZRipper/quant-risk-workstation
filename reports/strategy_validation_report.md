# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-09-07 to 2022-08-31 / 2022-09-01 to 2026-09-04

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.38 | 0.89 | 0.51 | -53.11% | -23.91% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.76 | 1.45 | 0.69 | -36.11% | -21.58% | 55.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.14 | 1.00 | 0.86 | -38.13% | -25.23% | 53.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.44 | 0.58 | 1.02 | -65.31% | -23.57% | 52.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.83 | 1.25 | 0.42 | -28.10% | -20.33% | 53.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.80 | 1.25 | 0.45 | -32.49% | -22.96% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.52 | 1.06 | 0.54 | -35.34% | -17.36% | 53.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.63 | 1.06 | 0.43 | -44.45% | -18.31% | 55.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.23 | 0.02 | 0.25 | -43.87% | -17.89% | 51.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.12 | 0.85 | 0.73 | -52.72% | -24.92% | 53.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.60 | 1.20 | 0.60 | -31.20% | -23.79% | 51.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.25 | 1.03 | 0.78 | -57.22% | -20.39% | 53.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.47 | 1.35 | 0.88 | -31.69% | -20.97% | 53.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.61 | 1.58 | 0.97 | -27.62% | -18.07% | 52.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.71 | 1.12 | 0.40 | -32.54% | -17.86% | 52.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.34 | 0.99 | 0.65 | -33.14% | -25.25% | 50.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.53 | 1.36 | 0.83 | -27.56% | -19.39% | 52.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.64 | 0.88 | 0.24 | -39.67% | -18.55% | 53.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.97 | 1.06 | 0.09 | -30.79% | -16.06% | 54.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.02 | 0.37 | 0.36 | -48.24% | -29.26% | 52.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
