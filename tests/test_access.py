import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.access_system import AccessSystem


class AccessSystemTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.system = AccessSystem(self.tmp.name)

    def tearDown(self):
        try:
            os.remove(self.tmp.name)
        except OSError:
            pass

    def test_happy_path_allows(self):
        result = self.system.verify({
            "event_id": "happy",
            "quality_score": 0.9,
            "liveness_score": 0.95,
            "embedding": [0.99, 0.05, 0.0],
            "network": "online"
        })
        self.assertEqual(result.decision, "allow")
        self.assertEqual(result.employee_id, "emp-4821")
        self.assertEqual(result.turnstile_command, "open")

    def test_spoof_goes_to_manual_review(self):
        result = self.system.verify({
            "event_id": "spoof",
            "quality_score": 0.9,
            "liveness_score": 0.30,
            "embedding": [0.99, 0.05, 0.0],
            "network": "online"
        })
        self.assertEqual(result.decision, "manual_review")
        self.assertEqual(result.turnstile_command, "keep_closed")

    def test_stale_offline_cache_goes_to_manual_review(self):
        result = self.system.verify({
            "event_id": "offline",
            "quality_score": 0.9,
            "liveness_score": 0.95,
            "embedding": [0.99, 0.05, 0.0],
            "network": "offline",
            "cache_age_minutes": 240
        })
        self.assertEqual(result.decision, "manual_review")
        self.assertIn("stale_edge_cache", result.reasons)

    def test_idempotency(self):
        event = {
            "event_id": "same",
            "quality_score": 0.9,
            "liveness_score": 0.95,
            "embedding": [0.99, 0.05, 0.0],
            "network": "online"
        }
        first = self.system.verify(event)
        second = self.system.verify(event)
        self.assertIs(first, second)


if __name__ == "__main__":
    unittest.main()
