import os, sys, tempfile, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.access_system import AccessSystem

class AccessSystemTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.system = AccessSystem(self.tmp.name)
    def tearDown(self):
        try: os.remove(self.tmp.name)
        except OSError: pass
    def test_happy_path_allows(self):
        r=self.system.verify({"event_id":"happy","employee_id":"emp-1","quality_score":0.9,"liveness_score":0.95,"match_score":0.85,"second_best_score":0.60,"network":"online"})
        self.assertEqual(r.decision,"allow"); self.assertEqual(r.turnstile_command,"open")
    def test_spoof_goes_to_manual_review(self):
        r=self.system.verify({"event_id":"spoof","employee_id":"emp-1","quality_score":0.9,"liveness_score":0.30,"match_score":0.95,"second_best_score":0.20,"network":"online"})
        self.assertEqual(r.decision,"manual_review"); self.assertEqual(r.turnstile_command,"keep_closed")
    def test_idempotency(self):
        event={"event_id":"same","employee_id":"emp-1","quality_score":0.9,"liveness_score":0.95,"match_score":0.85,"second_best_score":0.60,"network":"online"}
        first=self.system.verify(event); second=self.system.verify(event); self.assertIs(first,second)

if __name__ == "__main__": unittest.main()
