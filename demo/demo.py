import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.access_system import AccessSystem

system = AccessSystem(os.path.join(ROOT, "logs", "access_events.jsonl"))

happy = {"event_id":"e-1001","employee_id":"emp-4821","quality_score":0.88,"liveness_score":0.95,"match_score":0.81,"second_best_score":0.64,"network":"online","cache_age_minutes":5}
risky = {"event_id":"e-1003","employee_id":"emp-4821","quality_score":0.90,"liveness_score":0.35,"match_score":0.91,"second_best_score":0.40,"network":"online","cache_age_minutes":5}

print("=== HAPPY PATH ===")
print(json.dumps(system.verify(happy).__dict__, ensure_ascii=False, indent=2))
print("\n=== RISKY PATH ===")
print(json.dumps(system.verify(risky).__dict__, ensure_ascii=False, indent=2))
