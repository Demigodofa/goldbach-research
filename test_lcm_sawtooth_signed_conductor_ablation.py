import unittest

from lcm_sawtooth_signed_conductor_ablation import (
    classify_conductor_ablation,
    project_signed_conductor_ablation_receipt,
)


class LcmSawtoothSignedConductorAblationTests(unittest.TestCase):
    def test_classifier_requires_both_magnitude_and_upper_location(self):
        lower_largest = (
            {"excluded_conductor": 2, "parameter_shift": -.006},
            {"excluded_conductor": 11, "parameter_shift": .004},
        )
        result = classify_conductor_ablation(lower_largest, (11,))
        self.assertTrue(result["magnitude_falsifier_passes"])
        self.assertFalse(result["upper_half_location_falsifier_passes"])
        self.assertFalse(result["sparse_upper_conductor_hypothesis_passes"])

        upper_largest = (
            {"excluded_conductor": 2, "parameter_shift": -.004},
            {"excluded_conductor": 11, "parameter_shift": .006},
        )
        result = classify_conductor_ablation(upper_largest, (11,))
        self.assertTrue(result["sparse_upper_conductor_hypothesis_passes"])

    def test_classifier_guards_empty_rows_and_threshold(self):
        with self.assertRaises(ValueError):
            classify_conductor_ablation((), ())
        with self.assertRaises(ValueError):
            classify_conductor_ablation(
                ({"excluded_conductor": 2, "parameter_shift": 0},),
                (), 0)

    def test_m127_rejects_single_sparse_upper_conductor_control(self):
        receipt = project_signed_conductor_ablation_receipt(127)
        ranked = sorted(
            receipt["rows"],
            key=lambda row: abs(row["parameter_shift"]),
            reverse=True)
        self.assertAlmostEqual(
            receipt["baseline_best_parameter"], .2795716513419446)
        self.assertEqual(
            tuple(row["excluded_conductor"] for row in ranked[:4]),
            (55, 78, 143, 77))
        self.assertEqual(receipt["largest_influence_conductor"], 55)
        self.assertAlmostEqual(
            receipt["largest_absolute_parameter_shift"],
            .0009974649895388987)
        self.assertFalse(receipt["magnitude_falsifier_passes"])
        self.assertTrue(receipt["upper_half_location_falsifier_passes"])
        self.assertFalse(
            receipt["sparse_upper_conductor_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
