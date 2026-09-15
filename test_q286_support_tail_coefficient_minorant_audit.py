import json
import unittest
from pathlib import Path


class Q286SupportTailCoefficientMinorantAuditTests(unittest.TestCase):
    def test_coefficientwise_shortcut_is_falsified(self):
        path = Path(
            "evidence/q286-support-tail-coefficient-minorant-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(
            receipt["coefficientwise_tail_control_shortcut_falsified"])
        self.assertTrue(
            receipt["signed_prime_pair_distribution_still_required"])
        self.assertFalse(receipt["signed_tail_control_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

        counts = receipt["target_residue_counts"]
        self.assertEqual(counts["total_even_residues"], 5005)
        self.assertEqual(counts["partial_coefficients_all_positive"], 0)
        self.assertEqual(counts["full_coefficients_all_positive"], 0)
        self.assertEqual(counts["separated_tail_control_passes"], 0)

        full = receipt["global_unit_ratio_summaries"]["full"]
        partial = receipt["global_unit_ratio_summaries"][
            "principal_plus_dominant"]
        tail = receipt["global_unit_ratio_summaries"]["support_tail"]
        self.assertLess(full["minimum"], 0)
        self.assertLess(partial["minimum"], 0)
        self.assertLess(tail["minimum"], 0)
        self.assertGreater(full["maximum"], 0)
        self.assertGreater(partial["maximum"], 0)
        self.assertGreater(tail["maximum"], 0)

        self.assertEqual(
            sorted(receipt["tail_support_labels"]),
            ["11", "13", "5", "5x13", "7"],
        )


if __name__ == "__main__":
    unittest.main()
