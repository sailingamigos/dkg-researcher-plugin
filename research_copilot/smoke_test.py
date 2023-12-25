"""Unit tests"""

import unittest
from maestro import load_knowledge_assets, get_answer, perform_kmeans, perform_regression

class TestPlugin(unittest.TestCase):
    """Smoke test"""
    def test_ask_question(self):
        """Ask a question"""
        load_knowledge_assets ('knowledge_assets/semantic_scholar_blockchain')
        result = get_answer ('PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ScholarlyArticle .\n  ?paper :title ?title .\n} LIMIT 10')

        self.assertEqual(len(result), 10)

    def test_perform_kmeans(self):
        """Test kmeans functionality."""
        data = {
            'X': [[1, 2], [1, 4], [1, 0],
                  [10, 2], [10, 4], [10, 0]],
            'k': 2
        }
        result = perform_kmeans(data)
        self.assertEqual(len(result), data['k'])

    def test_perform_regression(self):
        """Test logistic regression functionality."""
        data = { 
            "X": [2020, 2021, 2022, 2023],
            "y": [146859, 84948, 20204, 1599],
            "predict_data": [2024, 2025, 2026]
        }
        result = perform_regression(data)
        print(result)
        self.assertEqual(len(result), len(data['predict_data']))


# Run the test
if __name__ == "__main__":
    unittest.main()
