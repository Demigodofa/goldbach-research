import random
import unittest

from weighted_lag_graph_lemma import weighted_geometric_variance_bound


class WeightedLagGraphLemmaTests(unittest.TestCase):
    def test_irregular_boundary_graph_obeys_bound(self):
        result = weighted_geometric_variance_bound(
            (0.7, 1.1, 0.9, 1.4),
            (2.0, 1.0, 3.0, 0.5),
            ((0, 1, 1.2), (0, 2, 0.3), (1, 3, 2.1)))
        self.assertTrue(result["inequality_verified_numerically"])
        self.assertGreater(result["edge_degree_factor"], 0)
        self.assertLessEqual(
            result["variance_lower_bound"],
            result["weighted_edge_geometric_mean"] + 1e-12)

    def test_constant_ratios_give_exact_bound(self):
        result = weighted_geometric_variance_bound(
            (0.37, 0.37, 0.37), (2.0, 3.0, 5.0),
            ((0, 1, 4.0), (1, 2, 1.0)))
        self.assertAlmostEqual(result["weighted_vertex_variance"], 0.0)
        self.assertAlmostEqual(result["variance_lower_bound"], 0.37)
        self.assertAlmostEqual(result["weighted_edge_geometric_mean"], 0.37)

    def test_seeded_random_weighted_graphs_obey_bound(self):
        generator = random.Random(20260910)
        for _ in range(200):
            size = 8
            ratios = [generator.random() * 3 for _ in range(size)]
            weights = [0.1 + generator.random() * 2 for _ in range(size)]
            edges = [(index, index + 1, 0.1 + generator.random() * 2)
                     for index in range(size - 1)]
            edges.extend((index, index + 2, 0.1 + generator.random() * 2)
                         for index in range(size - 2))
            result = weighted_geometric_variance_bound(
                ratios, weights, edges)
            self.assertTrue(result["inequality_verified_numerically"])
            self.assertLessEqual(
                result["variance_lower_bound"],
                result["weighted_edge_geometric_mean"] + 1e-12)

    def test_invalid_data_are_rejected(self):
        with self.assertRaises(ValueError):
            weighted_geometric_variance_bound((1.0,), (1.0,), ())
        with self.assertRaises(ValueError):
            weighted_geometric_variance_bound(
                (1.0, -1.0), (1.0, 1.0), ((0, 1, 1.0),))
        with self.assertRaises(ValueError):
            weighted_geometric_variance_bound(
                (1.0, 1.0), (1.0, 1.0), ((0, 2, 1.0),))


if __name__ == "__main__":
    unittest.main()
