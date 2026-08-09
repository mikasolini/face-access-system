import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


@dataclass
class Decision:
    event_id: str
    decision: str
    employee_id: str | None
    match_score: float
    margin_to_second_best: float
    reasons: List[str]
    turnstile_command: str
    requires_human_review: bool
    degraded_mode: bool


class AccessSystem:
    def __init__(self, log_path="logs/access_events.jsonl", employee_db=None):
        self.log_path = log_path
        self.processed: Dict[str, Decision] = {}
        self.employee_db = employee_db or {
            "emp-4821": [1.0, 0.0, 0.0],
            "emp-7310": [0.70, 0.70, 0.0],
            "emp-9002": [0.0, 1.0, 0.0],
        }

    def match_embedding(self, query_embedding: List[float]) -> Tuple[str | None, float, float]:
        scored = [
            (employee_id, cosine_similarity(query_embedding, embedding))
            for employee_id, embedding in self.employee_db.items()
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        best_id, best_score = scored[0]
        second_score = scored[1][1] if len(scored) > 1 else 0.0
        return best_id, best_score, second_score

    def verify(self, event: dict) -> Decision:
        event_id = event["event_id"]

        # Idempotency: повторное событие не должно повторно открыть турникет.
        if event_id in self.processed:
            return self.processed[event_id]

        quality = float(event.get("quality_score", 1.0))
        liveness = float(event.get("liveness_score", 1.0))
        network = event.get("network", "online")
        cache_age = int(event.get("cache_age_minutes", 0))
        query_embedding = event.get("embedding", [0.0, 0.0, 0.0])

        best_id, match, second = self.match_embedding(query_embedding)
        margin = match - second
        degraded = network != "online"
        reasons = []

        if liveness < 0.70:
            decision = "manual_review"
            reasons.append("liveness_low")
        elif quality < 0.60:
            decision = "manual_review"
            reasons.append("quality_low")
        elif degraded and cache_age > 60:
            decision = "manual_review"
            reasons.append("stale_edge_cache")
        elif match >= 0.80 and margin >= 0.10:
            decision = "allow"
            reasons.extend(["quality_ok", "liveness_ok", "match_above_allow_threshold"])
        elif match >= 0.60:
            decision = "manual_review"
            reasons.append("match_uncertain")
        else:
            decision = "deny"
            reasons.append("match_below_threshold")

        result = Decision(
            event_id=event_id,
            decision=decision,
            employee_id=best_id if decision == "allow" else None,
            match_score=round(match, 4),
            margin_to_second_best=round(margin, 4),
            reasons=reasons,
            turnstile_command="open" if decision == "allow" else "keep_closed",
            requires_human_review=decision == "manual_review",
            degraded_mode=degraded,
        )

        self.processed[event_id] = result
        self._audit(result)
        return result

    def _audit(self, result: Decision):
        directory = os.path.dirname(self.log_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")
