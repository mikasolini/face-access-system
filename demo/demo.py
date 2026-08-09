import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.access_system import AccessSystem

system = AccessSystem(os.path.join(ROOT, "logs", "access_events.jsonl"))

happy_event = {
    "event_id": "e-1001",
    "quality_score": 0.88,
    "liveness_score": 0.95,
    "embedding": [0.99, 0.05, 0.0],
    "network": "online",
    "cache_age_minutes": 5
}

risky_event = {
    "event_id": "e-1003",
    "quality_score": 0.90,
    "liveness_score": 0.35,
    "embedding": [0.99, 0.05, 0.0],
    "network": "online",
    "cache_age_minutes": 5
}

print("=== HAPPY PATH ===")
print(json.dumps(system.verify(happy_event).__dict__, ensure_ascii=False, indent=2))

print("\n=== RISKY PATH ===")
print(json.dumps(system.verify(risky_event).__dict__, ensure_ascii=False, indent=2))
