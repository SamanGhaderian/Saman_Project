import numpy as np
import umap


def compute_umap(distance_matrix, n_neighbors=5):
    """
    Convert DTW distance matrix → 2D coordinates
    """

    if len(distance_matrix) == 0:
        return np.array([])

    reducer = umap.UMAP(
        n_neighbors=min(n_neighbors, len(distance_matrix) - 1),
        metric="precomputed",
        random_state=42
    )

    embedding = reducer.fit_transform(distance_matrix)

    return embedding