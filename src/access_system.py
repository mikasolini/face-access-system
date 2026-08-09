import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List

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
    def __init__(self, log_path="logs/access_events.jsonl"):
        self.log_path = log_path
        self.processed: Dict[str, Decision] = {}

    def verify(self, event: dict) -> Decision:
        event_id = event["event_id"]
        if event_id in self.processed:
            return self.processed[event_id]

        quality = float(event.get("quality_score", 1.0))
        liveness = float(event.get("liveness_score", 1.0))
        match = float(event.get("match_score", 0.0))
        second = float(event.get("second_best_score", 0.0))
        margin = match - second
        network = event.get("network", "online")
        cache_age = int(event.get("cache_age_minutes", 0))
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
            reasons += ["quality_ok", "liveness_ok", "match_above_allow_threshold"]
        elif match >= 0.60:
            decision = "manual_review"
            reasons.append("match_uncertain")
        else:
            decision = "deny"
            reasons.append("match_below_threshold")

        result = Decision(
            event_id=event_id,
            decision=decision,
            employee_id=event.get("employee_id") if decision == "allow" else None,
            match_score=match,
            margin_to_second_best=margin,
            reasons=reasons,
            turnstile_command="open" if decision == "allow" else "keep_closed",
            requires_human_review=decision == "manual_review",
            degraded_mode=degraded,
        )
        self.processed[event_id] = result
        self._audit(result)
        return result

    def _audit(self, result: Decision):
        os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")
