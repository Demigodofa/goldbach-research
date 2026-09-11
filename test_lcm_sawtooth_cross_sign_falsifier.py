import unittest

from lcm_sawtooth_cross_sign_falsifier import (
    complete_energy_diagonal_sign_falsifier,
)


class LcmSawtoothCrossSignFalsifierTests(unittest.TestCase):
    def test_explicit_interval_has_positive_cross_excess(self):
        receipt = complete_energy_diagonal_sign_falsifier()
        self.assertGreater(receipt["complete_energy_over_diagonal"], 1.43)
        self.assertGreater(
            receipt["positive_cross_excess_over_diagonal"], .43)
        self.assertTrue(
            receipt["universal_nonpositive_mobius_cross_term_falsified"])
        self.assertFalse(receipt["project_scaled_cross_sign_theorem_proved"])


if __name__ == "__main__":
    unittest.main()
