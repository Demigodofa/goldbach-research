"""Carryover tests: prior AP output is proof data, never a trusted status bit."""
import copy
import unittest

import stacked_cover as sc


def extending_source() -> dict:
    """A two-target source whose verified AP output also reaches 10, 12, 14."""
    return {
        "schema": 1, "method": "stacked_prime_AP_certificates",
        "first_even": 6, "last_even": 8, "count": 2, "palette_limit": 10,
        "steps": [2], "covered_count": 2, "unresolved": [],
        "certificate_count": 1, "status": "certified",
        "certificates": [{
            "kind": "prime_AP_sum",
            "left": {"first": 3, "step": 2, "count": 3},
            "right": {"first": 3, "step": 2, "count": 3},
            "output": {"first": 6, "step": 2, "count": 5},
            "newly_covered": 2,
        }],
    }


class CarryoverTests(unittest.TestCase):
    def test_carry_membership_and_reverification(self):
        source=extending_source()
        self.assertEqual(sc.verify_block(source)["covered_count"],2)
        target=sc.cover_block(10,3,palette_limit=10,carry_from=source)
        self.assertEqual(target["carry_mode"],"enabled")
        self.assertEqual(target["carried_covered_count"],3)
        self.assertEqual(target["unresolved"],[])
        self.assertEqual(sc.verify_block(target)["covered_count"],3)

    def test_full_carry_skips_fresh_generation(self):
        target=sc.cover_block(10,3,palette_limit=10,carry_from=extending_source())
        self.assertTrue(target["fresh_generation_skipped"])
        self.assertEqual(target["fresh_certificate_count"],0)
        self.assertEqual(target["certificate_count"],1)

    def test_malformed_carry_is_rejected(self):
        bad=extending_source()
        bad["certificates"][0]["left"]["first"]=9
        with self.assertRaises(ValueError):
            sc.cover_block(10,3,palette_limit=10,carry_from=bad)
        with self.assertRaises(ValueError):
            sc.cover_block(10,3,palette_limit=10,carry_from={"status":"certified"})

    def test_carried_metadata_is_recomputed_and_checked(self):
        target=sc.cover_block(10,3,palette_limit=10,carry_from=extending_source())
        for field,value in [
            ("carry_mode","disabled"),
            ("carried_covered_count",2),
            ("carried_certificate_count",2),
            ("fresh_covered_count",1),
            ("fresh_certificate_count",1),
            ("fresh_generation_skipped",False),
        ]:
            forged=copy.deepcopy(target)
            forged[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                sc.verify_block(forged)
        forged=copy.deepcopy(target)
        del forged["fresh_certificate_count"]
        with self.assertRaises(ValueError):
            sc.verify_block(forged)

    def test_carried_proof_data_is_reconstructed_not_aliased(self):
        source=extending_source()
        target=sc.cover_block(10,3,palette_limit=10,carry_from=source)
        target["certificates"][0]["left"]["first"]=9
        self.assertEqual(source["certificates"][0]["left"]["first"],3)
        self.assertEqual(sc.verify_block(source)["covered_count"],2)
        with self.assertRaises(ValueError):
            sc.verify_block(target)

    def test_carried_and_fresh_certificates_compose(self):
        source=extending_source()
        # This target is only partly reached by the carried AP, forcing fresh work.
        target=sc.cover_block(10,5,palette_limit=20,carry_from=source)
        self.assertGreater(target["carried_covered_count"],0)
        self.assertGreater(target["fresh_certificate_count"],0)
        self.assertEqual(sc.verify_block(target)["covered_count"],5)
        forged=copy.deepcopy(target)
        forged["certificates"][0]["output"]["count"]=4
        with self.assertRaises(ValueError):
            sc.verify_block(forged)


if __name__=="__main__":
    unittest.main()
