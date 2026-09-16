import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/goldbach-semantic-route-graph.json")


class GoldbachSemanticRouteGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.nodes = {node["id"]: node for node in cls.graph["nodes"]}
        cls.edges = {
            (edge["source"], edge["relation"], edge["target"])
            for edge in cls.graph["edges"]
        }

    def test_graph_is_derived_not_authoritative(self):
        self.assertEqual(
            self.graph["status"], "GRAPH_current_goldbach_semantic_route")
        self.assertFalse(self.graph["goldbach_proved"])
        self.assertFalse(self.graph["semantic_graph_authoritative"])
        self.assertIn("Derived navigation graph only",
                      self.graph["authority_boundary"])
        self.assertIn("REFRESH_HANDOFF.md", self.graph["human_linear_sources"])

    def test_live_bridge_target_and_l2_hold_are_explicit(self):
        raw = self.nodes["theorem-target:raw-adverse-drag"]
        pointwise = self.nodes["theorem-target:pointwise-adverse-drag"]
        l2 = self.nodes["hold:l2-logical-bridge"]

        self.assertEqual(raw["status"], "live_unproved")
        self.assertEqual(pointwise["status"], "live_unproved")
        self.assertTrue(raw["finite_rows_pass_gate"])
        self.assertEqual(raw["worst_checked_target"], 1124642)
        self.assertTrue(pointwise["universal_bound_open"])
        self.assertFalse(l2["logical_bridge_confirmed"])
        self.assertEqual(l2["row_local_cap_violations"], 120)

    def test_broad_translation_falsifier_narrows_to_source_window(self):
        falsifier = self.nodes["finite-falsifier:broad-phase-translation"]
        source = self.nodes["finite-diagnostic:source-admissible-window"]

        self.assertEqual(falsifier["scale_modulus"], 149)
        self.assertEqual(falsifier["prime_modulus"], 163)
        self.assertEqual(falsifier["active_row_start"], 1)
        self.assertLess(falsifier["slack"], 0.0)
        self.assertTrue(source["all_source_starts_pass"])
        self.assertEqual(source["source_start_failure_count"], 0)
        self.assertIn(
            (
                "finite-falsifier:broad-phase-translation",
                "narrows-to",
                "finite-diagnostic:source-admissible-window",
            ),
            self.edges,
        )

    def test_acceptance_rule_blocks_finite_closeout(self):
        rule = self.nodes["rule:finite-evidence-not-acceptance"]

        self.assertIn("another finite horizon pass", rule["invalid_closeouts"])
        self.assertIn(
            ("rule:finite-evidence-not-acceptance",
             "blocks-closeout-of",
             "target:goldbach"),
            self.edges,
        )
        self.assertIn(
            ("finite-diagnostic:source-admissible-window",
             "not-acceptance-for",
             "target:goldbach"),
            self.edges,
        )

    def test_pointwise_target_has_proof_obligation_edges(self):
        required = {
            target for source, relation, target in self.edges
            if source == "theorem-target:pointwise-adverse-drag"
            and relation == "requires"
        }

        self.assertEqual(required, {
            "proof-obligation:1",
            "proof-obligation:2",
            "proof-obligation:3",
            "proof-obligation:4",
        })
        self.assertIn("Define the covered even-target class",
                      self.nodes["proof-obligation:1"]["statement"])
        self.assertIn("Prove A_-(N)<M(N)",
                      self.nodes["proof-obligation:3"]["statement"])

    def test_node_and_edge_counts_are_pinned(self):
        self.assertEqual(self.graph["node_count"], len(self.graph["nodes"]))
        self.assertEqual(self.graph["edge_count"], len(self.graph["edges"]))
        self.assertEqual(self.graph["node_count"], 13)
        self.assertEqual(self.graph["edge_count"], 19)

    def test_projection_views_capture_churn_and_thin_frontiers(self):
        views = self.graph["projection_views"]

        self.assertEqual(
            {
                item["name"]
                for item in views["by_theorem_attempt"]
            },
            {
                "raw adverse-drag bridge",
                "aggregate L2 bridge",
                "metric-soft source-window route",
            },
        )
        self.assertIn(
            "hold:l2-logical-bridge",
            views["by_result_state"]["hold"])
        self.assertEqual(
            views["churn_or_low_return_flags"][0]["area"],
            "normalized aggregate L2 finite scans")
        frontier_areas = {
            item["area"] for item in views["thin_or_frontier_flags"]
        }
        self.assertIn("source-window implication theorem", frontier_areas)
        self.assertIn(
            "universal pointwise raw adverse-drag bound", frontier_areas)

    def test_branch_map_has_nexus_live_hold_and_dead_ends(self):
        branch = self.graph["projection_views"]["branch_map"]

        self.assertEqual(branch["nexus"], "target:goldbach")
        self.assertEqual(branch["trunk"], "gate:current-bridge-acceptance")
        self.assertEqual(
            {item["id"] for item in branch["live_branches"]},
            {"branch:raw-adverse-drag", "branch:source-window"},
        )
        raw_branch = [
            item for item in branch["live_branches"]
            if item["id"] == "branch:raw-adverse-drag"
        ][0]
        self.assertEqual(raw_branch["twigs"], [
            "proof-obligation:1",
            "proof-obligation:2",
            "proof-obligation:3",
            "proof-obligation:4",
        ])
        self.assertEqual(
            branch["held_branches"][0]["id"], "branch:aggregate-l2")
        self.assertEqual(
            {item["id"] for item in branch["dead_ends"]},
            {
                "dead-end:broad-all-translation-dominance",
                "dead-end:finite-evidence-acceptance",
            },
        )


if __name__ == "__main__":
    unittest.main()
