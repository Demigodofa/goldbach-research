import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/q286-cap-homogeneity-boundary-audit.json")


class Q286CapHomogeneityBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q286_cap_homogeneity_boundary",
        )
        self.assertTrue(self.receipt["finite_logic_audit_only"])
        self.assertFalse(
            self.receipt["homogeneous_cap_standalone_bridge_proved"])
        self.assertFalse(self.receipt["positive_mass_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_homogeneous_cap_is_not_standalone(self):
        form = self.receipt["logical_forms"]["raw_homogeneous_cap"]
        self.assertEqual(form["classification"], "homogeneous_cap_control")
        self.assertIn("true but non-creative", form["zero_mass_status"])
        self.assertIn("useful only after positive mass",
                      form["bridge_status"])

    def test_strict_raw_gap_remains_standalone_shape(self):
        form = self.receipt["logical_forms"]["strict_raw_gap"]
        self.assertEqual(
            form["classification"],
            "standalone_noncircular_theorem_shape",
        )
        self.assertIn("false at T_N=0", form["zero_mass_status"])
        self.assertEqual(form["bridge_status"], "still_unproved")

    def test_cap_examples_remain_calibration_only(self):
        inherited = self.receipt["cap_window_inherited"]
        self.assertIn(".125", inherited["finite_fit_examples"])
        table = {
            item["route"]: item["decision"]
            for item in self.receipt["decision_table"]
        }
        self.assertEqual(table["finite caps .125/.126/.13"],
                         "calibration_only")
        self.assertEqual(
            table["universal homogeneous cap max(0,-U_d)<=k*T_N"],
            "not_standalone",
        )

    def test_route_correction_names_next_obligation(self):
        correction = self.receipt["route_correction"]
        self.assertTrue(correction["cap_sensitivity_still_useful"])
        self.assertIn("Do not present homogeneous caps alone",
                      correction["corrected_next_obligation"])


if __name__ == "__main__":
    unittest.main()
