import unittest

import numpy as np

from divisor_full_frame_probe import (
    _frame_receipt,
    _totient,
    finite_full_frame_probe,
    single_modulus_full_frame_probe,
)


class DivisorFullFrameProbeTests(unittest.TestCase):
    def test_totient(self):
        self.assertEqual([_totient(n) for n in (1, 2, 6, 30)], [1, 1, 2, 8])

    def test_frame_implication(self):
        frame = np.array([2.0, 3.0])
        ideal = np.diag(frame)
        exact = ideal + np.array([[-.2, .1], [.1, .3]])
        receipt = _frame_receipt(exact, ideal, frame)
        self.assertTrue(receipt["finite_lower_frame_certificate_survives"])
        self.assertGreaterEqual(
            receipt["actual_exact_over_frame_eigenvalue_min"] + 1e-12,
            receipt["proved_exact_over_frame_lower"])

    def test_finite_and_single_receipts(self):
        finite = finite_full_frame_probe(32000, modulus_limit=3)
        single = single_modulus_full_frame_probe(1009, 5, 9, 3, 8)
        self.assertGreaterEqual(finite["ideal_over_frame_eigenvalue_min"], 1-1e-10)
        self.assertGreaterEqual(single["ideal_over_frame_eigenvalue_min"], 1-1e-10)


if __name__ == "__main__":
    unittest.main()
