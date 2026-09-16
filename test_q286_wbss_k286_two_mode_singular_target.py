import json
import unittest
from pathlib import Path


class Q286WbssK286TwoModeSingularTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-two-mode-singular-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_target_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_k286_two_mode_singular_target_unproved")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["two_mode_pointwise_lower_bound_proved"])
        self.assertFalse(receipt["residual_singular_moment_cap_proved"])
        self.assertFalse(
            receipt["twisted_prime_pair_moment_theorem_proved"])
        self.assertFalse(receipt["k286_pointwise_lower_bound_proved"])

    def test_top_two_singular_numbers_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["top_two_summary"]
        singular = receipt["singular_values"]

        self.assertAlmostEqual(singular[0], 3.597046733129315, places=12)
        self.assertAlmostEqual(singular[1], 2.8233430589589674, places=12)
        self.assertAlmostEqual(summary["top_two_l2"], 4.572746573875274,
                               places=12)
        self.assertAlmostEqual(summary["tail_l2"], 0.7164353938945424,
                               places=12)
        self.assertAlmostEqual(summary["total_l2"], 4.628530101718351,
                               places=12)
        self.assertAlmostEqual(
            summary["top_two_energy_fraction"],
            0.9760410444893588,
            places=12)
        self.assertLess(summary["full_reconstruction_relative_error"],
                        1e-12)

    def test_two_mode_split_has_exact_functional_notation(self):
        receipt = self.load_receipt()
        notation = receipt["notation"]
        split = receipt["sufficient_two_mode_split"]

        self.assertIn("delta_{alpha,beta}(N)",
                      notation["normalized_moment"])
        self.assertIn("sigma_j*u_j(alpha)*vh_j(beta)",
                      notation["svd_decomposition"])
        self.assertIn("Re sum_j sigma_j*mu_j(N)",
                      notation["exact_functional"])
        self.assertAlmostEqual(
            split["tail_adverse_bound_under_global_cap"],
            0.02722757770861337,
            places=12)
        self.assertAlmostEqual(
            split["two_mode_floor_required_if_tail_has_global_cap"],
            -0.14867615917424493,
            places=12)

    def test_mode_rows_expose_vectors_without_promoting_theorem(self):
        receipt = self.load_receipt()
        rows = receipt["mode_rows"]

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["mode_index"], 1)
        self.assertEqual(rows[1]["mode_index"], 2)
        for row in rows:
            self.assertEqual(len(row["left_vector_top_entries_mod_11"]), 5)
            self.assertEqual(len(row["right_vector_top_entries_mod_13"]), 5)
            self.assertEqual(
                len(row["top_scaled_character_pair_coefficients"]), 8)
            self.assertAlmostEqual(
                row["normalized_mode_frobenius_norm"], 1.0, places=12)
        self.assertIn("not a theorem", receipt["status_boundary"])
        self.assertIn("This proves no such moment theorem",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
