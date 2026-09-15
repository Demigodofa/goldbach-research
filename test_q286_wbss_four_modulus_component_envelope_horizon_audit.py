import json
import unittest
from pathlib import Path


class Q286WbssFourModulusComponentEnvelopeHorizonAuditTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-component-envelope-horizon-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["per_modulus_supremum_theorem_proved"])
        self.assertFalse(
            receipt["one_sided_signed_concentration_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertFalse(receipt["universal_negative_drag_bound_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite fixture fits only",
                      receipt["residual_absorption_boundary"])

    def test_component_suprema_are_expected_horizon_values(self):
        receipt = self.load_receipt()
        suprema = receipt["component_adverse_suprema"]

        self.assertAlmostEqual(suprema["70"], 0.11808088288936758,
                               places=12)
        self.assertAlmostEqual(suprema["130"], 0.00932108976691037,
                               places=12)
        self.assertAlmostEqual(suprema["154"], 0.08239931832908774,
                               places=12)
        self.assertAlmostEqual(suprema["286"], 0.12228599640255161,
                               places=12)
        self.assertAlmostEqual(
            receipt["component_adverse_supremum_sum"],
            0.3320872873879173,
            places=12)

    def test_componentwise_envelope_survives_horizon(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["componentwise_envelope_survives_horizon"])
        self.assertFalse(receipt["componentwise_route_blocked"])
        self.assertEqual(summary["row_count"], 232)
        self.assertEqual(summary["componentwise_envelope_positive_count"],
                         232)
        self.assertEqual(summary["componentwise_envelope_nonpositive_count"],
                         0)
        self.assertEqual(receipt["holdout"]["target_minimum"], 1036248)
        self.assertEqual(receipt["holdout"]["target_maximum"], 1115822)

    def test_tightest_row_is_minimum_local_main_row(self):
        receipt = self.load_receipt()
        row = receipt["holdout"]["summary"][
            "tightest_componentwise_envelope_row"]

        self.assertEqual(row["target"], 1038176)
        self.assertAlmostEqual(row["local_uniform_main_term"],
                               0.717245423802844,
                               places=12)
        self.assertAlmostEqual(row["componentwise_envelope_expectation"],
                               0.38515813641492663,
                               places=12)
        self.assertAlmostEqual(row["componentwise_envelope_ratio"],
                               0.4630037032891566,
                               places=12)

    def test_component_supremum_source_targets_are_recorded(self):
        receipt = self.load_receipt()
        rows = receipt["component_adverse_supremum_rows"]

        self.assertEqual(rows["70"]["target"], 1076288)
        self.assertEqual(rows["130"]["target"], 1074592)
        self.assertEqual(rows["154"]["target"], 1055452)
        self.assertEqual(rows["286"]["target"], 1070252)


if __name__ == "__main__":
    unittest.main()
