import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json")


class MobiusMomentSquareDegree5Q46189PacketKernelSignTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_packet_kernel_sign_landscape")
        self.assertTrue(
            self.receipt["finite_packet_kernel_sign_landscape_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["coordinate00_residue_gap_sign_theorem_proved"])
        self.assertFalse(
            self.receipt["universal_kernel_sign_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_is_unique_kernel_overpayment_row(self):
        summary = self.receipt["landscape_summary"]
        classification = self.receipt["classification"]
        self.assertEqual(summary["same_source_denominator_count"], 35)
        self.assertEqual(summary["below_half_denominators"], [46189])
        self.assertEqual(summary["below_half_count"], 1)
        self.assertEqual(summary["off_diagonal_overpayment_count"], 1)
        self.assertEqual(
            summary["nonadverse_off_diagonal_overpayment_count"], 0)
        self.assertTrue(
            classification["q46189_unique_below_half_by_kernel_overpayment"])
        self.assertTrue(
            classification["all_nonadverse_rows_keep_diagonal_surplus"])

    def test_normalized_sign_values_are_stable(self):
        summary = self.receipt["landscape_summary"]
        qrow = self.receipt["q46189_row"]
        weakest = self.receipt["weakest_nonadverse_off_diagonal_row"]
        self.assertAlmostEqual(
            summary["q46189_off_diagonal_over_diagonal_half"],
            -1.0053819255304557,
            places=15,
        )
        self.assertEqual(
            summary["minimum_nonadverse_off_diagonal_denominator"],
            38038,
        )
        self.assertAlmostEqual(
            summary["minimum_nonadverse_off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15,
        )
        self.assertAlmostEqual(
            qrow["ratio_minus_half"],
            -0.002690962765227888,
            places=15,
        )
        self.assertAlmostEqual(
            weakest["ratio_minus_half"],
            0.07635340770691464,
            places=15,
        )

    def test_identity_reconstructs_ratio_minus_half(self):
        for row in self.receipt["rows"]:
            reconstructed = 0.5 * (
                1.0 + row["off_diagonal_over_diagonal_half"])
            self.assertAlmostEqual(
                reconstructed,
                row["ratio_minus_half"],
                places=12,
            )
            self.assertEqual(
                row["below_half"],
                row["off_diagonal_over_diagonal_half"] <= -1.0,
            )

    def test_next_action_targets_overpayment_exclusion(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(
            action["name"],
            "off-diagonal-overpayment exclusion theorem candidate")
        self.assertIn(
            "off_diagonal_total/diagonal_half > -1",
            action["mechanism"],
        )


if __name__ == "__main__":
    unittest.main()
