import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/goldbach-route-pattern-atlas.json")


class GoldbachRoutePatternAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_proof_boundaries(self):
        self.assertEqual(
            self.receipt["status"], "AUDIT_goldbach_route_pattern_atlas")
        self.assertTrue(self.receipt["finite_atlas_only"])
        self.assertFalse(self.receipt["goldbach_counterexample_found"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["universal_raw_pointwise_theorem_proved"])
        self.assertFalse(
            self.receipt["source_block_interaction_sign_theorem_proved"])

    def test_atlas_names_dead_and_live_route_shapes(self):
        names = {item["name"]: item for item in self.receipt["route_patterns"]}
        self.assertIn(
            "finite data is a falsifier and calibrator, not an acceptance condition",
            names,
        )
        self.assertEqual(
            names[
                "normalized or conditional mass routes collapse back to raw pointwise obligations"
            ]["classification"],
            "retired_as_standalone",
        )
        self.assertEqual(
            names[
                "adverse drag has the strongest finite q286 shape, but still needs a raw theorem"
            ]["classification"],
            "live_candidate",
        )
        self.assertEqual(
            names[
                "Q46189 scalar dots died; source-block matrix topology survived"
            ]["classification"],
            "live_candidate",
        )

    def test_next_action_is_source_block_sign_audit(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"],
                         "all-row source-block interaction sign audit")
        self.assertIn("all 34", action["smallest_test"])
        self.assertIn("input-side", action["prediction"])
        self.assertIn("output buckets", action["falsifier"])

    def test_disproof_lens_falsifies_mechanisms_not_goldbach(self):
        disproof = self.receipt["disproof_lens"]
        self.assertIn("No counterexample to Goldbach",
                      disproof["observed_result"])
        self.assertIn("normalized L2", disproof["observed_result"])
        self.assertGreaterEqual(len(disproof["next_falsifiers"]), 3)


if __name__ == "__main__":
    unittest.main()
