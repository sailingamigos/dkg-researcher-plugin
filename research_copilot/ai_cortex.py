"""AI cortext module."""

from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np

def kmeans_algorithm(X, k):
    """Perform kmeans algorithm"""
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

    labels = kmeans.labels_
    counts = np.bincount(labels)

    return counts


def linear_regression_algorithm(X, y, predict_data):
    """
    Perform linear regression.
    """
    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(predict_data).tolist()
    return predictions
