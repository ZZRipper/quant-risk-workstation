"""Strategy approval scorecard for research governance.

The scorecard converts validation, diversification and paper-trading evidence
into a transparent approval decision. It is intentionally rule-based for v1 so
each score can be explained to a supervisor or interviewer.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _scale(value: float, low: float, high: float) -> float:
    if high == low:
        return 0.0
    return _clamp((value - low) / (high - low) * 100)


def _decision(score: float) -> str:
    if score >= 80:
        return "Approve"
    if score >= 60:
        return "Watch"
    if score >= 40:
        return "Revise"
    return "Reject"


def _paper_metrics(paper_pnl_ledger: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    by_strategy: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in paper_pnl_ledger:
        by_strategy[str(row["strategyId"])].append(row)

    metrics = {}
    for strategy_id, rows in by_strategy.items():
        net_pnls = [float(row.get("netPnl", 0.0)) for row in rows]
        costs = [float(row.get("cost", 0.0)) for row in rows]
        turnovers = [float(row.get("turnover", 0.0)) for row in rows]
        metrics[strategy_id] = {
            "paperPnl": sum(net_pnls),
            "paperPositiveRate": sum(1 for value in net_pnls if value > 0) / len(net_pnls) * 100 if net_pnls else 0.0,
            "paperAvgCost": mean(costs) if costs else 0.0,
            "paperAvgTurnover": mean(turnovers) if turnovers else 0.0,
        }
    return metrics


def _correlation_risk(strategy_id: str, strategy_correlation: dict[str, object]) -> tuple[float, list[str]]:
    pairs = strategy_correlation.get("highCorrelationPairs", [])
    linked = []
    max_corr = 0.0
    for pair in pairs:
        if pair.get("leftId") == strategy_id:
            linked.append(str(pair.get("rightId")))
            max_corr = max(max_corr, abs(float(pair.get("correlation", 0.0))))
        elif pair.get("rightId") == strategy_id:
            linked.append(str(pair.get("leftId")))
            max_corr = max(max_corr, abs(float(pair.get("correlation", 0.0))))
    return max_corr, linked[:3]


def _component_scores(
    strategy: dict[str, object],
    validation: dict[str, object],
    paper: dict[str, float],
    max_corr: float,
) -> dict[str, float]:
    oos_sharpe = float(validation.get("outOfSampleSharpe", 0.0))
    sharpe_decay = float(validation.get("sharpeDecay", 0.0))
    oos_drawdown = float(validation.get("outOfSampleDrawdown", 0.0))
    oos_return = float(validation.get("outOfSampleReturn", 0.0))
    oos_hit = float(validation.get("outOfSampleHitRate", 0.0))
    cost_bps = float(strategy.get("costBps", 0.0))
    paper_pnl = paper.get("paperPnl", 0.0)
    paper_positive = paper.get("paperPositiveRate", 0.0)
    paper_turnover = paper.get("paperAvgTurnover", 0.0)
    dominant_beta = abs(float(validation.get("dominantFactorBeta", 0.0)))

    return {
        "oosPerformance": 0.65 * _scale(oos_sharpe, 0.0, 1.5) + 0.35 * _scale(oos_return, 0.0, 80.0),
        "robustness": _scale(sharpe_decay, -1.5, 0.25),
        "drawdownControl": _scale(oos_drawdown, -30.0, -5.0),
        "costEfficiency": 0.60 * (100 - _scale(cost_bps, 0.0, 4.0)) + 0.40 * (100 - _scale(paper_turnover, 0.0, 25.0)),
        "diversification": 100 - _scale(max_corr, 0.50, 0.90),
        "factorIndependence": 100 - _scale(dominant_beta, 0.25, 1.25),
        "paperBehavior": 0.55 * _scale(paper_pnl, -5000.0, 5000.0) + 0.45 * _scale(paper_positive, 35.0, 70.0),
        "hitRate": _scale(oos_hit, 40.0, 60.0),
    }


def _strengths_weaknesses(
    component_scores: dict[str, float],
    validation: dict[str, object],
    paper: dict[str, float],
    linked: list[str],
) -> tuple[list[str], list[str]]:
    strengths = []
    weaknesses = []

    if component_scores["oosPerformance"] >= 70:
        strengths.append("OOS performance remains strong")
    if component_scores["robustness"] >= 70:
        strengths.append("Limited Sharpe decay")
    if component_scores["drawdownControl"] >= 70:
        strengths.append("OOS drawdown is controlled")
    if component_scores["paperBehavior"] >= 65:
        strengths.append("Paper trading behavior is positive")
    if component_scores["diversification"] >= 70:
        strengths.append("Low recent correlation pressure")

    if component_scores["oosPerformance"] < 45:
        weaknesses.append("OOS performance is weak")
    if component_scores["robustness"] < 45:
        weaknesses.append("Sharpe decays materially out of sample")
    if component_scores["drawdownControl"] < 45:
        weaknesses.append("OOS drawdown is high")
    if component_scores["costEfficiency"] < 45:
        weaknesses.append("Cost or turnover drag is high")
    if component_scores["diversification"] < 45 and linked:
        weaknesses.append(f"High correlation with {', '.join(linked)}")
    if component_scores["factorIndependence"] < 45:
        weaknesses.append(f"Crowded factor beta: {validation.get('dominantFactor', 'N/A')}")
    if paper.get("paperPnl", 0.0) < 0:
        weaknesses.append("Paper-period PnL is negative")

    return strengths[:3], weaknesses[:3]


def build_strategy_scorecard(
    strategies: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
    paper_pnl_ledger: list[dict[str, object]],
    strategy_correlation: dict[str, object],
) -> list[dict[str, object]]:
    validation_by_id = {str(row["id"]): row for row in validation_rows}
    paper_by_id = _paper_metrics(paper_pnl_ledger)
    rows = []

    weights = {
        "oosPerformance": 0.25,
        "robustness": 0.18,
        "drawdownControl": 0.15,
        "costEfficiency": 0.12,
        "diversification": 0.10,
        "factorIndependence": 0.08,
        "paperBehavior": 0.08,
        "hitRate": 0.04,
    }

    for strategy in strategies:
        strategy_id = str(strategy["id"])
        validation = validation_by_id.get(strategy_id, {})
        paper = paper_by_id.get(strategy_id, {})
        max_corr, linked = _correlation_risk(strategy_id, strategy_correlation)
        components = _component_scores(strategy, validation, paper, max_corr)
        score = sum(components[name] * weight for name, weight in weights.items())
        decision = _decision(score)
        strengths, weaknesses = _strengths_weaknesses(components, validation, paper, linked)
        rows.append({
            "id": strategy_id,
            "name": strategy["name"],
            "sleeve": strategy["sleeve"],
            "score": round(score, 1),
            "decision": decision,
            "recommendedAction": {
                "Approve": "Eligible for paper allocation review",
                "Watch": "Keep paper allocation and monitor decay",
                "Revise": "Research changes before adding capital",
                "Reject": "Remove from active candidate set",
            }[decision],
            "components": {key: round(value, 1) for key, value in components.items()},
            "oosSharpe": validation.get("outOfSampleSharpe", 0.0),
            "oosDrawdown": validation.get("outOfSampleDrawdown", 0.0),
            "sharpeDecay": validation.get("sharpeDecay", 0.0),
            "paperPnl": round(paper.get("paperPnl", 0.0), 2),
            "maxCorrelation": round(max_corr, 3),
            "dominantFactor": validation.get("dominantFactor", "N/A"),
            "strengths": strengths,
            "weaknesses": weaknesses,
        })

    rows.sort(key=lambda row: float(row["score"]), reverse=True)
    return rows
