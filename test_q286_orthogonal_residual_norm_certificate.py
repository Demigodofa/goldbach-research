import json
import unittest
from pathlib import Path


class Q286OrthogonalResidualNormCertificateTests(unittest.TestCase):
    def test_norm_certificate_is_valid_but_too_blunt(self):
        path = Path("evidence/q286-orthogonal-residual-norm-certificate.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("Cauchy-Schwarz", receipt["candidate_cone"])
        self.assertIn("<nu_N,h_a>", receipt["decision"])

        summary = receipt["summary"]
        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(summary["selected_residue_count"], 7)
        self.assertEqual(summary["certified_target_count"], 0)
        self.assertEqual(summary["certified_targets"], [])
        self.assertEqual(summary["actual_full_positive_target_count"], 5)
        self.assertEqual(
            summary["actual_full_positive_not_norm_certified_targets"],
            [94856, 1222142, 1240888, 1242118, 1379072])
        self.assertEqual(summary["actual_bad_branch_targets"], [14138, 14996])
        self.assertEqual(summary["maximum_reconstruction_error"], 0.0)
        self.assertGreater(
            summary["norm_certificate_ratio_summary"]["minimum"], 1.0)

        for row in receipt["target_rows"]:
            self.assertFalse(row["passes_orthogonal_residual_norm_certificate"])
            self.assertAlmostEqual(
                row["aligned_only_full_action_to_principal"]
                + row["orthogonal_residual_action_to_principal"],
                row["actual_full_action_to_principal_ratio"])


if __name__ == "__main__":
    unittest.main()
