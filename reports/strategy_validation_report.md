# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-09-27 to 2022-09-20 / 2022-09-21 to 2026-09-23

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.35 | 0.98 | 0.63 | -53.11% | -23.91% | 53.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.70 | 1.37 | 0.67 | -36.11% | -24.94% | 55.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.13 | 1.01 | 0.87 | -38.12% | -29.11% | 53.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.45 | 0.65 | 1.09 | -65.31% | -23.57% | 51.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.78 | 1.19 | 0.41 | -28.10% | -20.33% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.74 | 1.19 | 0.46 | -32.49% | -22.96% | 52.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.50 | 1.11 | 0.61 | -35.34% | -17.36% | 53.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.58 | 1.14 | 0.56 | -44.45% | -18.31% | 55.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.27 | 0.04 | 0.32 | -43.87% | -20.56% | 50.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.11 | 0.84 | 0.72 | -52.72% | -19.79% | 53.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.60 | 1.23 | 0.62 | -31.20% | -23.79% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.21 | 1.09 | 0.88 | -57.22% | -19.16% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.45 | 1.41 | 0.96 | -31.69% | -20.97% | 53.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.61 | 1.51 | 0.90 | -27.62% | -18.07% | 52.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.65 | 1.11 | 0.46 | -32.54% | -17.86% | 52.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.32 | 0.96 | 0.64 | -33.14% | -29.16% | 50.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.54 | 1.31 | 0.78 | -27.56% | -19.39% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.59 | 0.95 | 0.36 | -39.67% | -17.62% | 53.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.92 | 0.96 | 0.04 | -30.79% | -19.25% | 54.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.02 | 0.43 | 0.45 | -48.24% | -22.79% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
