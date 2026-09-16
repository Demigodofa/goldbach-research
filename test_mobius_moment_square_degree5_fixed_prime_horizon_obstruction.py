import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-fixed-prime-horizon-obstruction.json")


class MobiusMomentSquareDegree5FixedPrimeHorizonObstructionTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_fixed_prime_horizon_obstruction")
        self.assertEqual(self.receipt["answer"], "NO")
        self.assertTrue(
            self.receipt["fixed_prime_universal_target_obstructed"])
        self.assertTrue(
            self.receipt["elementary_interval_obstruction_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["prime_block_theorem_proved"])
        self.assertFalse(self.receipt["moving_prime_block_theorem_proved"])

    def test_weakest_sequence_is_imported_from_morphology(self):
        self.assertEqual(
            self.receipt["weakest_prime_counts"],
            {"379": 2, "461": 1, "599": 4})
        self.assertEqual(
            self.receipt["p599_observed_weak_scales"],
            [331, 353, 379, 383])

    def test_fixed_prime_599_horizon_is_exact(self):
        horizon = self.receipt["fixed_prime_horizons"]["599"]
        self.assertEqual(horizon["minimum_integer_scale_M"], 300)
        self.assertEqual(horizon["maximum_integer_scale_M"], 599)
        self.assertEqual(horizon["integer_scale_count"], 300)
        self.assertEqual(horizon["first_impossible_integer_scale_M"], 600)
        self.assertEqual(
            self.receipt["p599_integer_admissible_scale_span"], [300, 599])
        self.assertEqual(
            self.receipt["p599_first_impossible_integer_scale_M"], 600)
        self.assertIn("ceil(599/2)=300", horizon["calculation"])

    def test_replacement_target_is_moving_prime_block_control(self):
        target = self.receipt["candidate_replacement_theorem_target"]
        self.assertEqual(
            target["name"],
            "moving source-start prime-block lower-frame control")
        self.assertIn("p=p(M)", target["mechanism"])
        self.assertEqual(target["novelty_label"], "new-to-this-task")


if __name__ == "__main__":
    unittest.main()
