import json
import unittest
from pathlib import Path


class Q286WbssMultiplicativeResidualScheduleAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-multiplicative-residual-schedule-audit.json"
        ).read_text(encoding="utf-8"))

    def row_by_keep_count(self, receipt, count):
        for row in receipt["schedule"]:
            if row["kept_character_count"] == count:
                return row
        raise AssertionError(f"missing schedule row for {count}")

    def test_receipt_is_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"], "HOLD_residual_character_bound_required")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["residual_character_bound_proved"])
        self.assertFalse(receipt["multiplicative_character_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(receipt["acceptance_condition"][
            "finite_evidence_is_acceptance_condition"])
        self.assertIn("AdverseDrag(N) < LocalMain(N)", receipt[
            "acceptance_condition"]["unnormalized_target"])

    def test_active_nonzero_character_count_and_local_main(self):
        receipt = self.load_receipt()

        self.assertEqual(receipt["active_nonzero_character_count"], 122)
        self.assertAlmostEqual(receipt["minimum_local_main"],
                               0.6039353780830684,
                               places=12)

    def test_99_percent_package_residual_is_not_small(self):
        receipt = self.load_receipt()
        row = self.row_by_keep_count(receipt, 77)

        self.assertAlmostEqual(row["selected_energy_fraction"],
                               0.9907751703358407,
                               places=12)
        self.assertAlmostEqual(
            row["crude_probability_discrepancy_residual_bound_sum"],
            46.26350760893429,
            places=9)
        self.assertGreater(
            row["crude_residual_to_minimum_local_main_ratio"], 76.0)
        self.assertFalse(row["coefficient_residual_eliminated"])

    def test_near_complete_package_still_needs_residual_theorem(self):
        receipt = self.load_receipt()
        row = self.row_by_keep_count(receipt, 120)

        self.assertAlmostEqual(row["selected_energy_fraction"],
                               0.9999960134030969,
                               places=12)
        self.assertAlmostEqual(
            row["crude_probability_discrepancy_residual_bound_sum"],
            1.3182746959839886,
            places=12)
        self.assertGreater(
            row["crude_probability_discrepancy_residual_bound_sum"],
            row["minimum_local_main"])

    def test_full_active_package_eliminates_coefficient_residual(self):
        receipt = self.load_receipt()
        row = self.row_by_keep_count(receipt, 122)

        self.assertAlmostEqual(row["selected_energy_fraction"], 1.0,
                               places=12)
        self.assertEqual(
            row["crude_probability_discrepancy_residual_bound_sum"], 0.0)
        self.assertTrue(row["coefficient_residual_eliminated"])

    def test_decision_names_required_residual_or_full_package(self):
        receipt = self.load_receipt()

        self.assertIn("explicit residual character theorem",
                      receipt["decision"])
        self.assertIn("full active nonzero multiplicative-character package",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
