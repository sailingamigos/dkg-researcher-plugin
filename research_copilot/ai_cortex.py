"""AI cortext module."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import numpy as np

def kmeans_algorithm(X, k):
    """Perform kmeans algorithm"""
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(X)

    scaler = StandardScaler()
    tfidf_matrix_standardized = scaler.fit_transform(tfidf_matrix.toarray())

    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix_standardized)

    result = []
    for i, data in enumerate(X):
        result.append({'X': data, 'cluster': int(cluster_labels[i])})

    return result

def linear_regression_algorithm(X, y, predict_data):
    """
    Perform linear regression.
    """
    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(predict_data).tolist()
    return predictions
