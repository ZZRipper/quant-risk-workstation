# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-11-21 to 2022-11-14 / 2022-11-15 to 2026-11-17

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.32 | 0.99 | 0.67 | -53.11% | -23.91% | 53.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.72 | 1.24 | 0.52 | -36.11% | -31.56% | 55.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.17 | 0.76 | 0.59 | -38.13% | -32.96% | 53.0% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.40 | 0.43 | 0.82 | -66.86% | -23.57% | 51.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.76 | 1.02 | 0.26 | -28.39% | -24.81% | 52.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.68 | 1.05 | 0.37 | -32.49% | -24.24% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.52 | 0.96 | 0.44 | -35.34% | -17.36% | 54.0% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.57 | 1.00 | 0.43 | -44.45% | -18.31% | 56.0% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.20 | -0.30 | -0.10 | -44.50% | -29.86% | 50.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.04 | 0.94 | 0.90 | -52.72% | -17.30% | 53.8% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.62 | 1.04 | 0.42 | -33.92% | -23.79% | 51.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.16 | 1.13 | 0.96 | -57.22% | -19.16% | 54.0% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.47 | 1.26 | 0.78 | -31.69% | -20.97% | 52.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.50 | 1.35 | 0.84 | -27.62% | -18.07% | 52.1% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.69 | 1.02 | 0.33 | -34.55% | -17.86% | 51.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.31 | 0.75 | 0.45 | -33.71% | -31.73% | 49.9% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.47 | 1.10 | 0.63 | -27.56% | -24.18% | 52.0% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.62 | 0.69 | 0.06 | -39.67% | -19.01% | 52.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 0.94 | 0.99 | 0.05 | -30.79% | -19.68% | 54.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | -0.04 | 0.26 | 0.30 | -53.80% | -22.48% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
