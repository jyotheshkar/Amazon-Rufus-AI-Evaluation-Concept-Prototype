"""Synchronous contracts for shared evidence and deterministic fixture arithmetic."""
import unittest
from backend.agents.judge_agent import JudgeAgent
from backend.agents.rufus_agent import RufusAgent


class AgentEvidenceTests(unittest.TestCase):
    def test_agents_receive_identical_catalogue_evidence(self):
        products = [{"name": "Fixture", "specs": {"battery": "30 hours"},
                     "description": "Synthetic evidence"}]
        answer = RufusAgent(use_mock=True)._build_product_context(products)
        judge = JudgeAgent(use_mock=True)._build_product_context(products)
        self.assertEqual(answer, judge)
        self.assertIn("battery: 30 hours", judge)

    def test_all_fixture_overalls_are_recomputed(self):
        agent = JudgeAgent(use_mock=True)
        expected = {None: 8.8, "missing_info_trap": 7.0, "price_trap": 7.3,
                    "contradiction_query": 7.6, "ambiguous_intent": 7.9,
                    "pressure_scenario": 8.2}
        for scenario, overall in expected.items():
            with self.subTest(scenario=scenario):
                self.assertEqual(agent._mock_response(scenario)["overall"], overall)

    def test_adversarial_fixture_does_not_change_standard(self):
        agent = JudgeAgent(use_mock=True)
        agent._mock_response("missing_info_trap")
        self.assertEqual(agent._mock_response()["hallucination"]["score"], 9)

    def test_fixture_currency_is_decoded_as_utf8(self):
        result = RufusAgent(use_mock=True)._mock_response("fixture", [])
        self.assertIn("£279.99", result["answer"])


if __name__ == "__main__":
    unittest.main()
