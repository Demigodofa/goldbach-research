import json
import unittest
from pathlib import Path


class Q286SignedSupportTailControlDefinitionTests(unittest.TestCase):
    def test_definition_preserves_tail_sign_orientation(self):
        path = Path(
            "evidence/q286-signed-support-tail-control-definition.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(
            receipt["signed_support_tail_control_definition_written"])
        self.assertTrue(receipt["pure_three_support_harmless_tail_falsified"])
        self.assertFalse(receipt["signed_tail_control_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

        theorem = receipt["candidate_theorem"]
        self.assertEqual(theorem["objects"]["period"], 10010)
        self.assertIn("A_N = P_N + D_N + R_N",
                      theorem["objects"]["action_decomposition"])
        self.assertIn("r_N > -eta_a(N)",
                      " ".join(theorem["sufficient_inequalities"]))

        known = receipt["evidence_inputs"]["known_extremals"]
        self.assertEqual(known["tail_changes_sign_decision_count"], 16)
        self.assertEqual(
            known["tail_flip_orientation"],
            "negative_tail_kills_positive_principal_plus_top_three")
        self.assertEqual(len(known["negative_tail_kill_targets"]), 16)
        self.assertEqual(known["positive_tail_rescue_targets"], [])

        tail_moduli = sorted(
            row["natural_modulus"]
            for row in receipt["evidence_inputs"]["tail_support_rows"])
        self.assertEqual(tail_moduli, [10, 14, 22, 26, 130])


if __name__ == "__main__":
    unittest.main()
