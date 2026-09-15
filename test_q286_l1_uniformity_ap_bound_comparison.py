import json
import unittest
from pathlib import Path


class Q286L1UniformityApBoundComparisonTests(unittest.TestCase):
    def test_bmor_comparison_demotes_blunt_l1_route(self):
        path = Path("evidence/q286-l1-uniformity-ap-bound-comparison.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(receipt["goldbach_proved"])
        self.assertEqual(
            receipt["l1_candidate_source"],
            "evidence\\q286-cone-duality-l1-uniformity-candidate.json")
        self.assertEqual(
            receipt["source"]["tables"]["constants"]["sha256"],
            "ce5d67887f3e95a4b76b5cfcf9037187c0399357d6848a2f24e65cadf03f443c")
        self.assertEqual(
            receipt["source"]["tables"]["thresholds"]["sha256"],
            "022e8bbda7f3cbce9b2950e40450c37dbf6d34f9457f8a70ef57ad0d0366c0c3")

        rows = {row["q"]: row for row in receipt["modulus_rows"]}
        self.assertEqual(set(rows), {143, 286, 10010})
        self.assertEqual(rows[10010]["phi_q"], 2880)
        self.assertGreater(
            rows[10010]["theta_probability_l1_proxy_at_x_theta"],
            receipt["l1_bad_radius_summary"]["maximum"])
        self.assertGreater(
            rows[10010]["pi_probability_l1_proxy_at_x_pi"],
            receipt["l1_bad_radius_summary"]["maximum"])
        self.assertGreater(
            rows[10010]["theta_x_needed_for_l1_radius"]["minimum"],
            1e18)
        self.assertIn("binary strict-central", receipt["decision"])


if __name__ == "__main__":
    unittest.main()
