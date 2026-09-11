import unittest

import numpy as np

from lcm_sawtooth_local_kloosterman import (
    _local_inverse_difference_matrix,
    local_kloosterman_receipt,
)


class LocalKloostermanTests(unittest.TestCase):
    def test_zero_frequency_is_complete_graph_without_loops(self):
        matrix = _local_inverse_difference_matrix(7, 0)
        self.assertLess(
            float(np.max(np.abs(matrix - (np.ones((6, 6)) - np.eye(6))))),
            1e-12)

    def test_local_norm_gates(self):
        receipt = local_kloosterman_receipt()
        self.assertEqual(receipt["primes"], (5, 7, 11, 13))
        expected_norms = {
            5: 2.545008902,
            7: 3.87311445,
            11: 5.34930158,
            13: 5.99625179,
        }
        for prime, expected in expected_norms.items():
            row = receipt["rows"][prime]
            self.assertAlmostEqual(
                row["zero_frequency_operator_norm"], prime - 2, places=12)
            self.assertAlmostEqual(
                row["maximum_nonzero_frequency_operator_norm"],
                expected, places=7)
            self.assertLessEqual(
                row["maximum_nonzero_frequency_operator_norm"],
                row["weil_bound"] + 1e-12)
            self.assertLessEqual(row["maximum_compression_excess"], 1e-12)
            self.assertTrue(row["all_nonzero_frequencies_have_one_norm"])
            self.assertTrue(row["local_kloosterman_norm_gate_passes"])
        self.assertTrue(receipt["all_local_kloosterman_norm_gates_pass"])
        self.assertFalse(receipt["exact_crt_source_transfer_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            local_kloosterman_receipt(primes=(9,))
        with self.assertRaises(ValueError):
            local_kloosterman_receipt(tolerance=-1)


if __name__ == "__main__":
    unittest.main()
