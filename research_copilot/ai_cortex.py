"""AI cortex module."""

from sklearn.feature_extraction.text import TfidfVectorizer # pylint: disable=import-error
from sklearn.cluster import KMeans # pylint: disable=import-error
from sklearn.preprocessing import StandardScaler # pylint: disable=import-error
from sklearn.linear_model import LinearRegression # pylint: disable=import-error
from sentence_transformers import SentenceTransformer, util # pylint: disable=import-error
import numpy as np # pylint: disable=import-error
import torch

def kmeans_algorithm(X, k):
    """
    Perform K-means clustering on the input data.

    Args:
        X (list): List of input data.
        k (int): Number of clusters to create.

    Returns:
        list: List of dictionaries containing input data and assigned cluster label.
    """
    # TF-IDF vectorization
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(X)

    # Standardize TF-IDF matrix
    scaler = StandardScaler()
    tfidf_matrix_standardized = scaler.fit_transform(tfidf_matrix.toarray())

    # K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix_standardized)

    result = []
    for i, data in enumerate(X):
        result.append({'X': data, 'cluster': int(cluster_labels[i])})

    return result

def linear_regression_algorithm(X, y, predict_data):
    """
    Perform linear regression and make predictions.

    Args:
        X (array-like): Training data.
        y (array-like): Target values.
        predict_data (array-like): Data to make predictions on.

    Returns:
        list: Predicted values.
    """
    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(predict_data).tolist()
    return predictions

def vector_search_algorithm(user_query, paper_embeddings):
    """
    Perform vector-based search using cosine similarity.

    Args:
        user_query (str): User's query.
        paper_embeddings (list): List of paper embeddings.

    Returns:
        list: Sorted indices of papers by similarity score in descending order.
    """
    specter_model = SentenceTransformer('sentence-transformers/allenai-specter')
    query_embedding = specter_model.encode(user_query, convert_to_tensor=True)

    # Compute cosine similarities between the user query and the papers
    paper_embeddings = [torch.tensor(embedding) for embedding in paper_embeddings]
    similarities = [util.pytorch_cos_sim(query_embedding, paper_embedding).item() for paper_embedding in paper_embeddings]

    # Sort the papers by similarity score in descending order and get the indices
    sorted_indices = np.argsort(similarities)[::-1]
    return sorted_indices
