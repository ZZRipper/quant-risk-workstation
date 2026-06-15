# Strategy Validation Report

## Scope

This report validates the current prototype stock-alpha strategies using the same no-lookahead backtest outputs that feed the dashboard.

- Macro regime: Rising growth + rising inflation (Inflationary expansion)
- Macro source: Partial FRED + Yahoo ETF proxy
- Fallback note: Missing FRED series: T10YIE, DGS10, BAA10YM, VIXCLS
- IS/OOS split: 2016-06-16 to 2022-06-09 / 2022-06-10 to 2026-06-12

## Validation Table

| ID | Strategy | IS Sharpe | OOS Sharpe | Sharpe Decay | IS DD | OOS DD | OOS Hit Rate | OOS Status | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| STR-01 | WQ Alpha 001 - Short-Term Reversal | 0.37 | 0.71 | 0.34 | -53.11% | -26.73% | 51.8% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-02 | WQ Alpha 004 - Rank Momentum | 0.96 | 1.51 | 0.55 | -36.11% | -19.66% | 55.5% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-03 | WQ Alpha 006 - Volume Price Divergence | 0.17 | 1.13 | 0.96 | -38.13% | -20.77% | 54.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-04 | WQ Alpha 012 - Open-Close Pressure | -0.43 | 0.61 | 1.04 | -62.64% | -23.57% | 52.4% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-05 | WQ Alpha 021 - Trend Stability | 0.96 | 1.16 | 0.19 | -28.10% | -20.33% | 52.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-06 | WQ Alpha 024 - Delayed Momentum | 0.87 | 1.24 | 0.37 | -32.49% | -22.96% | 52.7% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-07 | WQ Alpha 028 - Correlation Reversal | 0.56 | 0.83 | 0.28 | -35.34% | -19.38% | 52.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-08 | WQ Alpha 032 - VWAP Mean Reversion | 0.66 | 0.93 | 0.27 | -44.45% | -22.44% | 54.8% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-09 | WQ Alpha 041 - High-Low Range | -0.20 | 0.02 | 0.22 | -43.87% | -16.24% | 51.5% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-10 | WQ Alpha 043 - Volume Acceleration | 0.18 | 0.73 | 0.56 | -52.72% | -29.93% | 53.4% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-11 | WQ Alpha 051 - Decay Momentum | 0.73 | 1.18 | 0.45 | -30.18% | -23.79% | 52.1% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-12 | WQ Alpha 055 - Turnover Reversal | 0.21 | 0.82 | 0.61 | -57.22% | -27.40% | 52.6% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-13 | WQ Alpha 060 - Price Volume Rank | 0.55 | 1.32 | 0.77 | -31.69% | -20.97% | 53.2% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-14 | WQ Alpha 071 - Composite Rank | 0.69 | 1.38 | 0.69 | -27.62% | -18.07% | 52.6% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-15 | WQ Alpha 078 - Correlation Break | 0.78 | 0.75 | -0.03 | -32.54% | -17.86% | 50.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-16 | WQ Alpha 083 - Range Momentum | 0.41 | 1.03 | 0.62 | -33.14% | -25.25% | 50.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |
| STR-17 | WQ Alpha 088 - Liquidity Adjusted Momentum | 0.59 | 1.33 | 0.74 | -27.56% | -19.39% | 52.7% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-18 | WQ Alpha 092 - Delayed Reversal | 0.65 | 0.91 | 0.26 | -39.67% | -20.85% | 53.9% | Watch | OOS performance is usable but needs monitoring before more capital is assigned. |
| STR-19 | WQ Alpha 096 - Risk Controlled Momentum | 1.19 | 1.04 | -0.15 | -30.79% | -16.44% | 53.9% | Pass | OOS performance remains positive with acceptable drawdown degradation. |
| STR-20 | WQ Alpha 101 - Close To Open Reversal | 0.12 | 0.19 | 0.07 | -48.24% | -37.16% | 52.5% | Fail | OOS performance or drawdown indicates the signal may not generalize. |

## Methodology Notes

- Each strategy ranks the same large-cap universe and selects the latest top holdings from its own signal.
- Signals use only information available before the return period being evaluated: t-1 signal determines day t holdings and day t PnL.
- The backtest engine stays in cash until each strategy has enough minimum history.
- Current stock allocation inside each strategy is top-N equal weight.
- Transaction costs use 5 bps for buys and 5 bps for sells.
- Current universe and strategy formulas are prototype research assumptions.
- The current public-data version still has survivorship bias because the equity universe is not point-in-time.
- Current FRED macro data can contain revision bias; production-grade macro backtests should use ALFRED vintage data.
