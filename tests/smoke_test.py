"""Unit tests"""

import unittest

from plugin.maestro import load_data, get_answer

class TestPlugin(unittest.TestCase):
    """Smoke test"""
    def test_ask_question(self):
        """Ask a question"""
        load_data ('assets_bot/cache/assets.jsonld')

        result = get_answer ({
            "question": "Select top 10 triples",
            "sparqlQuery": """PREFIX : <http://schema.org/> SELECT ?s ?p ?o WHERE {
                                ?s ?p ?o .
                            } LIMIT 10""",
            "entities": [""],
            "relations": [""]
        })

        self.assertEqual(len(result), 10)

# Run the test
if __name__ == "__main__":
    unittest.main()
