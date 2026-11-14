"""Regressions for evidence parity and invalid model-output contamination."""
import copy
import unittest
from backend.agents.product_context import build_product_context
from backend.agents.scoring import validate_judgement, weighted_overall


def judgement():
    return {name: {"score": value, "reasoning": "fixture"} for name, value in
            (("helpfulness", 8), ("accuracy", 9), ("hallucination", 9), ("safety", 10))}


class ScoreBoundaryTests(unittest.TestCase):
    def test_overall_is_computed_not_trusted(self):
        data = judgement()
        data["overall"] = 99
        result = validate_judgement(data)
        self.assertEqual(result["overall"], 8.8)
        self.assertEqual(data["overall"], 99)

    def test_bad_scores_fail_instead_of_polluting_metrics(self):
        for value in (True, "8", None, -1, 11, 10 ** 400, float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=value):
                data = judgement()
                data["accuracy"]["score"] = value
                with self.assertRaises(ValueError):
                    validate_judgement(data)

    def test_missing_dimensions_and_invalid_root_are_rejected(self):
        data = judgement()
        del data["safety"]
        for item in (data, [], None):
            with self.subTest(item=item):
                with self.assertRaises(ValueError):
                    weighted_overall(item)

    def test_boundary_values_are_valid(self):
        for value in (0, 10, 5.5):
            data = judgement()
            for item in data.values():
                item["score"] = value
            self.assertEqual(weighted_overall(data), value)

    def test_invalid_metadata_and_reasoning_are_rejected(self):
        for field, value in (("summary", []), ("adversarial_triggered", "false"),
                             ("failure_mode_detected", "made-up")):
            data = judgement()
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_judgement(data)
        data = judgement()
        data["accuracy"]["reasoning"] = None
        with self.assertRaises(ValueError):
            validate_judgement(data)

    def test_evidence_contains_specs_and_description(self):
        products = [{"name": "Fixture headphones", "price": 100,
                     "description": "A synthetic product", "specs":
                     {"battery": "30 hours", "connections": ["USB", "Bluetooth"], "unknown": None}}]
        before = copy.deepcopy(products)
        evidence = build_product_context(products)
        self.assertIn("battery: 30 hours", evidence)
        self.assertIn("connections: USB, Bluetooth", evidence)
        self.assertIn("A synthetic product", evidence)
        self.assertNotIn("unknown:", evidence)
        self.assertEqual(products, before)

    def test_empty_and_missing_specs(self):
        self.assertIn("No relevant products", build_product_context([]))
        self.assertIn("N/A", build_product_context([{"name": "Fixture", "specs": None}]))


if __name__ == "__main__":
    unittest.main()
