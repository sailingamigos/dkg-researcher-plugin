"""Unit tests for Maestro module"""

import unittest
from maestro import load_knowledge_assets, get_answer, perform_kmeans, perform_regression, perform_vector_search, connect_to_otnode

class TestMaestro(unittest.TestCase):
    """Test cases for Maestro module."""

    def test_primary_repository(self):
        """Test primary repository."""
        response = get_answer({
            'repository': 1,
            'scholarlyArticleSparqlQuery': 'PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ScholarlyArticle .\n  ?paper :title ?title .\n} LIMIT 10',
            'arxivSparqlQuery': '',
        })
    
        (graph, repository, result) = response[0]

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'SemanticScholar')
        self.assertEqual(len(result), 10)

    def test_secondary_repository(self):
        """Test secondary repository."""
        response = get_answer({
            'repository': 2,
            'scholarlyArticleSparqlQuery': '',
            'arxivSparqlQuery': 'PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ArxivArticle .\n  ?paper :title ?title .\n} LIMIT 10',
        })

        (graph, repository, result) = response[0]

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'Arxiv')
        self.assertEqual(len(result), 10)
        
    def test_author_query(self):
        """Test author repository."""
        load_knowledge_assets('knowledge_assets/semantic_scholar_computer_vision')
        response = get_answer({
            'repository': 1,
            'scholarlyArticleSparqlQuery': 'PREFIX : <http://schema.org/>\nSELECT ?name WHERE {\n  ?article a :ScholarlyArticle .\n  ?article :title ?title .\n  FILTER(LCASE(?title) = '"automatic feature selection in neuroevolution"')\n  ?article :authors ?author .\n  ?author :name ?name .\n}',
            'arxivSparqlQuery': '',
        })

        (graph, repository, result) = response[0]

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'SemanticScholar')
        self.assertEqual(len(result), 2)

    def test_all_repository(self):
        """Test all repositories."""
        response = get_answer({
            'repository': 0,
            'scholarlyArticleSparqlQuery': 'PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ScholarlyArticle .\n  ?paper :title ?title .\n} LIMIT 10',
            'arxivSparqlQuery': 'PREFIX : <http://schema.org/>\nSELECT ?paper ?title WHERE {\n  ?paper a :ArxivArticle .\n  ?paper :title ?title .\n} LIMIT 10',
        })

        (graph, repository, result) = response[0]

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'SemanticScholar')
        self.assertEqual(len(result), 10)

        (graph, repository, result) = response[1]

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'Arxiv')
        self.assertEqual(len(result), 10)

    def test_perform_kmeans(self):
        """Test kmeans functionality."""
        abstracts = ['This paper discusses the applications of machine learning in healthcare research.',
                     'This research explores recent trends in natural language processing.',
                     'We present Fashion-MNIST, a new dataset comprising of 28x28 grayscale images of 70,000 fashion products from 10 categories, with 7,000 images per category. The training set has 60,000 images and the test set has 10,000 images. Fashion-MNIST is intended to serve as a direct drop-in replacement for the original MNIST dataset for benchmarking machine learning algorithms, as it shares the same image size, data format and the structure of training and testing splits. The dataset is freely available at this https URL',
                     'TensorFlow is a machine learning system that operates at large scale and in heterogeneous environments. Tensor-Flow uses dataflow graphs to represent computation, shared state, and the operations that mutate that state. It maps the nodes of a dataflow graph across many machines in a cluster, and within a machine across multiple computational devices, including multicore CPUs, general-purpose GPUs, and custom-designed ASICs known as Tensor Processing Units (TPUs). This architecture gives flexibility to the application developer: whereas in previous "parameter server" designs the management of shared state is built into the system, TensorFlow enables developers to experiment with novel optimizations and training algorithms. TensorFlow supports a variety of applications, with a focus on training and inference on deep neural networks. Several Google services use TensorFlow in production, we have released it as an open-source project, and it has become widely used for machine learning research. In this paper, we describe the TensorFlow dataflow model and demonstrate the compelling performance that TensorFlow achieves for several real-world applications',
                     'Machine learning addresses the question of how to build computers that improve automatically through experience. It is one of today’s most rapidly growing technical fields, lying at the intersection of computer science and statistics, and at the core of artificial intelligence and data science. Recent progress in machine learning has been driven both by the development of new learning algorithms and theory and by the ongoing explosion in the availability of online data and low-cost computation. The adoption of data-intensive machine-learning methods can be found throughout science, technology and commerce, leading to more evidence-based decision-making across many walks of life, including health care, manufacturing, education, financial modeling, policing, and marketing.']
        data = {
            'X': abstracts,
            'k': 3
        }
        result = perform_kmeans(data)
        self.assertEqual(len(result), len(abstracts))

    def test_perform_regression(self):
        """Test logistic regression functionality."""
        data = {
            "X": [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            "y": [166154, 139604, 200765, 95987, 141864, 263629, 195087, 262716, 169947, 151609, 600511, 725345, 655437, 646485, 464931, 493128, 165408, 97719, 26190, 2281,],
            "predict_data": [2024, 2025, 2026, 2027, 2028, 2029, 2030]
        }
        result = perform_regression(data)
        print(result)
        self.assertEqual(len(result), len(data['predict_data']))

    def test_vector_search(self):
        """Test vector search functionality."""
        data = {
            'question': 'meta learning'
        }
        response = perform_vector_search(data)
        (graph, repository, result) = response

        self.assertEqual(graph, 'DKG')
        self.assertEqual(repository, 'SemanticScholar')
        self.assertEqual(len(result), 3)
        print(result)

# Run the test
if __name__ == "__main__":
    unittest.main()
