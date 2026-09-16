import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/q286-one-sided-cap-sensitivity-audit.json")


class Q286OneSidedCapSensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q286_one_sided_cap_sensitivity",
        )
        self.assertTrue(self.receipt["finite_cap_sensitivity_audit_only"])
        self.assertFalse(self.receipt["per_modulus_supremum_theorem_proved"])
        self.assertFalse(
            self.receipt["one_sided_signed_concentration_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_uniform_cap_window_is_nonempty(self):
        window = self.receipt["uniform_cap_window"]
        self.assertTrue(window["nonempty_window"])
        self.assertLess(
            window["observed_uniform_cap_floor_inclusive"],
            window["strict_equal_cap_theorem_ceiling_exclusive"],
        )
        self.assertGreater(window["window_width"], 0.05)

    def test_125_126_13_fit_and_are_sufficient_if_universal(self):
        rows = {
            row["cap"]: row for row in self.receipt["cap_sensitivity"]
        }
        for cap in (0.125, 0.126, 0.13):
            self.assertTrue(rows[cap]["observed_fit_on_232_rows"])
            self.assertTrue(
                rows[cap][
                    "universal_equal_cap_would_be_sufficient_if_proved"])
            self.assertEqual(
                rows[cap]["classification"],
                "fits_finite_and_theorem_sufficient_if_universal",
            )

    def test_too_strict_and_too_loose_examples_are_classified(self):
        rows = {
            row["cap"]: row for row in self.receipt["cap_sensitivity"]
        }
        self.assertFalse(rows[0.12]["observed_fit_on_232_rows"])
        self.assertEqual(rows[0.12]["classification"],
                         "too_strict_for_observed_horizon")
        self.assertTrue(rows[0.18]["observed_fit_on_232_rows"])
        self.assertFalse(
            rows[0.18][
                "universal_equal_cap_would_be_sufficient_if_proved"])
        self.assertEqual(
            rows[0.18]["classification"],
            "fits_finite_but_not_sufficient_as_equal_cap",
        )

    def test_constant_ordering_explanation(self):
        text = self.receipt["interpretation_of_125_126_13"]["point"]
        self.assertIn(".125 is stricter than .126", text)
        self.assertIn("both are stricter than .13", text)


if __name__ == "__main__":
    unittest.main()
