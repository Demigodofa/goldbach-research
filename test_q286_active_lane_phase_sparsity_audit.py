import json
import unittest

from tools.build_q286_active_lane_phase_sparsity_audit import OUT


class Q286ActiveLanePhaseSparsityAuditTest(unittest.TestCase):

    def test_phase_sparsity_receipt_records_sparse_suffix(self):
        self.assertTrue(OUT.exists())
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        self.assertEqual(receipt["row_count"], 226)
        self.assertEqual(receipt["positive_count"], 83)
        self.assertEqual(receipt["nonpositive_count"], 143)
        self.assertEqual(receipt["sign_change_count_in_target_order"], 77)
        self.assertTrue(receipt["all_blocks_8_and_later_positive"])
        self.assertEqual(receipt["block_8_and_later_row_count"], 10)
        self.assertTrue(receipt["block_7_is_mixed"])

        suffix = receipt["pass_only_suffix_after_largest_failure"]
        self.assertEqual(suffix["threshold_target_exclusive"], 647392)
        self.assertEqual(suffix["first_suffix_target"], 650476)
        self.assertEqual(suffix["suffix_row_count"], 11)
        self.assertTrue(suffix["suffix_all_positive"])
        self.assertEqual(
            suffix["suffix_targets"],
            [650476, 658598, 733126, 741976, 775426, 782336,
             805682, 818528, 828418, 846632, 955832])

    def test_phase_sparsity_receipt_blocks_residue_only_explanation(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        residue = receipt["residue_mod_286_summary"]
        self.assertEqual(residue["residue_class_count"], 78)
        self.assertEqual(residue["pure_positive_class_count"], 12)
        self.assertEqual(residue["pure_nonpositive_class_count"], 32)
        self.assertEqual(residue["mixed_sign_class_count"], 34)
        self.assertAlmostEqual(
            receipt["correlations"]["log_target_vs_strict_margin"],
            0.7494686331045737)
        self.assertAlmostEqual(
            receipt["correlations"]["log_target_vs_channel_contribution"],
            0.7073559773555494)


if __name__ == "__main__":
    unittest.main()
