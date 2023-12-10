"""Unit tests"""

import unittest

from research_copilot.maestro import load_knowledge_assets, get_answer

class TestPlugin(unittest.TestCase):
    """Smoke test"""
    def test_ask_question(self):
        """Ask a question"""
        load_knowledge_assets ('knowledge_assets')
        result = get_answer ('PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ScholarlyArticle .\n  ?paper :title ?title .\n} LIMIT 10')

        self.assertEqual(len(result), 10)

# Run the test
if __name__ == "__main__":
    unittest.main()
