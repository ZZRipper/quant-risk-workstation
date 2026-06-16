# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + falling inflation (Risk-on)
- Macro source: FRED + Yahoo ETF proxy
- Fallback note: none
- IS/OOS split: 2016-06-20 to 2022-06-13 / 2022-06-14 to 2026-06-16

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.29 | 0.83 | 0.54 | -54.22% | -25.33% | 52.3% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.97 | 1.59 | 0.62 | -35.93% | -19.94% | 55.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.21 | 1.14 | 0.94 | -39.30% | -20.59% | 54.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.42 | 0.76 | 1.18 | -62.22% | -20.75% | 53.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.93 | 1.25 | 0.31 | -28.44% | -19.18% | 53.3% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.83 | 1.30 | 0.47 | -32.78% | -23.01% | 53.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.53 | 0.91 | 0.38 | -35.18% | -19.59% | 53.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.60 | 0.99 | 0.39 | -43.09% | -23.00% | 54.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.33 | 0.19 | 0.53 | -42.31% | -17.24% | 50.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.16 | 0.70 | 0.54 | -51.12% | -31.43% | 53.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.70 | 1.25 | 0.55 | -29.62% | -24.44% | 52.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.19 | 0.93 | 0.74 | -56.12% | -27.56% | 52.2% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.50 | 1.42 | 0.92 | -33.82% | -23.21% | 52.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.66 | 1.52 | 0.86 | -28.06% | -17.90% | 53.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.70 | 0.84 | 0.14 | -32.16% | -18.43% | 51.2% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.41 | 1.22 | 0.80 | -32.03% | -24.25% | 51.6% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.58 | 1.32 | 0.74 | -26.88% | -19.84% | 52.4% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.58 | 0.95 | 0.37 | -39.28% | -20.86% | 54.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.19 | 1.08 | -0.11 | -31.17% | -16.14% | 54.0% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.09 | 0.27 | 0.17 | -47.67% | -35.24% | 52.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
