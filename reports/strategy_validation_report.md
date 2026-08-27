# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-08-30 to 2022-08-23 / 2022-08-24 to 2026-08-26

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.38 | 0.84 | 0.46 | -53.11% | -24.38% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.79 | 1.43 | 0.64 | -36.11% | -21.58% | 55.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.16 | 0.99 | 0.83 | -38.13% | -22.87% | 53.3% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.39 | 0.49 | 0.88 | -65.31% | -23.57% | 51.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.85 | 1.16 | 0.31 | -28.10% | -20.33% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.83 | 1.15 | 0.32 | -32.49% | -22.96% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.56 | 1.01 | 0.45 | -35.34% | -17.59% | 53.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.66 | 1.02 | 0.36 | -44.45% | -21.38% | 55.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.19 | 0.01 | 0.19 | -43.87% | -17.89% | 51.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.17 | 0.82 | 0.65 | -52.72% | -27.38% | 53.7% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.62 | 1.17 | 0.55 | -31.20% | -23.79% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.28 | 0.96 | 0.68 | -57.22% | -24.53% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.49 | 1.30 | 0.81 | -31.69% | -20.97% | 53.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.63 | 1.49 | 0.86 | -27.62% | -18.07% | 52.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.73 | 1.09 | 0.35 | -32.54% | -17.86% | 52.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.36 | 0.92 | 0.56 | -33.14% | -25.25% | 50.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.54 | 1.32 | 0.78 | -27.56% | -19.39% | 52.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.66 | 0.85 | 0.19 | -39.67% | -20.01% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.01 | 1.02 | 0.01 | -30.79% | -16.06% | 54.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.04 | 0.31 | 0.26 | -48.24% | -32.10% | 52.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
