import json
import unittest
from pathlib import Path


class Q286WbssBauerWangSourceFitAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-bauer-wang-source-fit-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_source_fit_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SOURCE_FIT_Bauer_Wang_not_q286_raw_pointwise_bridge")
        self.assertFalse(receipt["bauer_wang_direct_bridge_found"])
        self.assertFalse(receipt["external_pointwise_bridge_found"])
        self.assertFalse(receipt["raw_weighted_witness_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("Source-fit HOLD only",
                      receipt["status_boundary"])

    def test_bauer_wang_quantifiers_are_almost_all(self):
        receipt = self.load_receipt()
        shape = receipt["bauer_wang_theorem_shape_from_metadata"]

        self.assertIn("almost all prime moduli",
                      shape["modulus_quantifier"])
        self.assertIn("almost all admissible b1",
                      shape["residue_quantifier"])
        self.assertIn("almost all integers n",
                      shape["target_quantifier"])
        self.assertIn("arithmetic progressions",
                      shape["method_note"])

    def test_required_q286_shape_is_every_n_raw_signed(self):
        receipt = self.load_receipt()
        required = receipt["q286_required_bridge_shape"]

        self.assertEqual(
            required["target_quantifier"],
            "every sufficiently large covered even N")
        self.assertIn("exact fixed q286", required["modulus"])
        self.assertIn("exact signed q286", required["weight"])
        self.assertIn("raw unnormalized", required["scale"])
        self.assertIn("N/3 < p < 2N/3", required["interval"])
        self.assertIn("cannot divide by T_N",
                      required["support_boundary"])

    def test_mismatches_block_direct_wakeup(self):
        receipt = self.load_receipt()
        mismatches = {row["id"]: row for row in receipt["mismatches"]}

        self.assertIn("almost_all_targets", mismatches)
        self.assertIn("almost_all_moduli_and_residues", mismatches)
        self.assertIn("positive_AP_pair_not_signed_q286_weight",
                      mismatches)
        self.assertIn("no_strict_central_or_finite_remainder_bridge",
                      mismatches)
        self.assertEqual(
            receipt["fit_summary"]["fit_to_q286_raw_pointwise_trigger"],
            "insufficient")
        self.assertFalse(
            receipt["fit_summary"]["reactivates_q286_signed_weight_lane"])

    def test_decision_moves_away_from_source_fit_retry(self):
        receipt = self.load_receipt()

        self.assertIn("closes as a direct q286 wake-up source",
                      receipt["decision"])
        self.assertIn("Stop retrying named AP-Goldbach source fit",
                      receipt["next_evidence_bearing_move"])
        self.assertIn("raw active-character theorem target",
                      receipt["next_evidence_bearing_move"])


if __name__ == "__main__":
    unittest.main()
