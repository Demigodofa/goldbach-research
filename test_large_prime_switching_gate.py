import unittest

from large_prime_switching_gate import (large_prime_log_vector,
                                        negative_cofactor_witness,
                                        prime_atom_log_vector,
                                        short_divisor_weight,
                                        switched_remainder_vector)


class LargePrimeSwitchingTests(unittest.TestCase):
    def test_truncated_mobius_weight_has_both_prime_atom_and_negative_composite(self):
        self.assertEqual(short_divisor_weight(1, 7), 1)
        self.assertEqual(short_divisor_weight(15, 7), -1)  # 1-1-1; 15>7

    def test_unique_large_prime_switch_is_exact(self):
        # P=22 has P^2>k.  For k=31*15 the unique large prime is 31,
        # and its cofactor has a_7(15)=-1.
        self.assertEqual(large_prime_log_vector(31 * 15, 7, 22), ((31, -1),))
        self.assertEqual(switched_remainder_vector(31 * 15, 7, 22), ((31, -1),))

    def test_prime_atom_is_separated_exactly(self):
        self.assertEqual(large_prime_log_vector(31, 7, 20), ((31, 1),))
        self.assertEqual(prime_atom_log_vector(31, 20), ((31, 1),))
        self.assertEqual(switched_remainder_vector(31, 7, 20), ())

    def test_negative_weight_blocks_direct_nonnegative_sieve_input(self):
        result = negative_cofactor_witness(3, 5, 7)
        self.assertEqual(result["weight"], -1)
        self.assertFalse(result["one_sided_sieve_usable"])

    def test_unique_large_factor_guard(self):
        with self.assertRaises(ValueError):
            large_prime_log_vector(35, 7, 5)  # 5^2 is not greater than 35


if __name__ == "__main__":
    unittest.main()
