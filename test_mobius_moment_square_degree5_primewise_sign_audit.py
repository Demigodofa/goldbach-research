import unittest

from tools.build_mobius_moment_square_degree5_primewise_sign_audit import (
    build_receipt,
    local_degree5_contributions,
)


class MobiusMomentSquareDegree5PrimewiseSignAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_local_degree5_contributions_uses_three_pairs(self):
        active = [[0.0 for _ in range(6)] for _ in range(6)]
        full = [[0.0 for _ in range(6)] for _ in range(6)]
        active[0][4] = active[4][0] = -3.0
        active[1][2] = active[2][1] = -5.0
        active[1][3] = active[3][1] = -7.0
        contributors = local_degree5_contributions(active, full)
        self.assertEqual(
            [(row["left_label"], row["right_label"]) for row in contributors],
            [("00", "12"), ("01", "02"), ("01", "11")])
        self.assertEqual(
            [row["half_frame_contribution"] for row in contributors],
            [-6.0, -10.0, -14.0])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "CHECK_degree5_primewise_sign_localization")
        self.assertTrue(
            self.receipt["finite_primewise_sign_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["primewise_sign_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_weak_block_primewise_contributors_are_negative(self):
        self.assertEqual(self.receipt["scale_modulus"], 167)
        self.assertEqual(self.receipt["prime_count"], 29)
        self.assertTrue(
            self.receipt["all_prime_degree5_totals_negative"])
        self.assertTrue(
            self.receipt["all_prime_component_contributors_negative"])
        self.assertEqual(
            self.receipt["degree5_total_sign_counts"],
            {"positive": 0, "zero": 0, "negative": 29})
        for summary in self.receipt["component_totals"].values():
            self.assertEqual(
                summary["sign_counts"],
                {"positive": 0, "zero": 0, "negative": 29})

    def test_component_totals_match_prior_burden(self):
        self.assertTrue(
            self.receipt[
                "component_totals_match_prior_burden_within_float_tolerance"])
        self.assertLessEqual(
            self.receipt[
                "maximum_abs_component_total_delta_from_prior_burden"],
            0.1)

    def test_extreme_rows_are_expected_primes(self):
        self.assertEqual(
            self.receipt["least_adverse_prime_row"]["prime_modulus"],
            181)
        self.assertEqual(
            self.receipt["most_adverse_prime_row"]["prime_modulus"],
            241)


if __name__ == "__main__":
    unittest.main()
