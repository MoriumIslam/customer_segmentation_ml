import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def train_kmeans_model(X, n_clusters=3, random_state=42, n_init=10):
    """
    Train KMeans model
    
    Parameters:
    - X: Preprocessed feature matrix
    - n_clusters: Number of clusters
    - random_state: Random seed for reproducibility
    - n_init: Number of times KMeans runs with different initializations
    
    Returns:
    - model: Trained KMeans model
    - labels: Cluster labels for each sample
    """
    model = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=n_init,
        max_iter=500,
        tol=1e-4
    )
    
    labels = model.fit_predict(X)
    
    return model, labels


def get_optimal_k_elbow(inertias, silhouette_scores=None, sensitivity=0.9):
    """
    Determine optimal K using elbow method with silhouette score consideration
    
    Parameters:
    - inertias: List of inertia values for K=2 to 10
    - silhouette_scores: List of silhouette scores for K=2 to 10
    - sensitivity: Sensitivity for detecting elbow (0-1)
    
    Returns:
    - optimal_k: Suggested K value
    """
    inertias = np.array(inertias)
    n_points = len(inertias)
    
    # If silhouette scores available, prioritize high silhouette score
    if silhouette_scores is not None and len(silhouette_scores) == len(inertias):
        silhouette_scores = np.array(silhouette_scores)
        # Find K with best silhouette score (highest is best)
        best_silhouette_idx = np.argmax(silhouette_scores)
        optimal_k = best_silhouette_idx + 2  # +2 because we start from K=2
        return optimal_k
    
    # Fallback to original elbow method
    differences = np.diff(inertias)
    second_diff = np.diff(differences)
    
    if len(second_diff) > 0:
        elbow_idx = np.argmax(second_diff) + 1
    else:
        elbow_idx = 0
    
    optimal_k = elbow_idx + 2
    
    # Ensure k is within bounds
    optimal_k = max(2, min(optimal_k, n_points + 1))
    
    return optimal_k


def evaluate_clustering(X, labels):
    """
    Evaluate clustering quality
    
    Returns: Dictionary with metrics
    """
    metrics = {
        "n_clusters": len(np.unique(labels)),
        "silhouette_score": float(silhouette_score(X, labels)),
        "cluster_distribution": {}
    }
    
    for cluster in np.unique(labels):
        count = np.sum(labels == cluster)
        pct = count / len(labels) * 100
        metrics["cluster_distribution"][f"Cluster_{cluster}"] = {
            "count": int(count),
            "percentage": float(pct)
        }
    
    return metrics
