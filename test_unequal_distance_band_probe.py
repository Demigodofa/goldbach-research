import unittest

from unequal_distance_band_probe import (
    _distance_edges,
    unequal_distance_bands,
)


class UnequalDistanceBandProbeTests(unittest.TestCase):
    def test_edges_cover_half_modulus(self):
        edges = _distance_edges(1009, 5)
        self.assertEqual(edges[:3], (0, 5, 10))
        self.assertEqual(edges[-1], 1009 // 2)
        self.assertTrue(all(a < b for a, b in zip(edges, edges[1:])))

    def test_bands_reconstruct_unequal_matrix(self):
        receipt = unequal_distance_bands(457, 3, 9, 2, 4)
        self.assertLess(receipt["unequal_reconstruction_error_max"], 1e-7)
        self.assertAlmostEqual(
            receipt["distance_bands"][-1][
                "cumulative_residual_over_equality"],
            receipt["final_raw_residual_over_equality"], places=10)
        self.assertFalse(receipt["near_H_localization_proved"])


if __name__ == "__main__":
    unittest.main()
