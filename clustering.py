import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN


# =====================================================
# Hierarchical clustering (existing baseline)
# =====================================================

def hierarchical_clustering(
        distance_matrix,
        patient_ids,
        n_clusters=3):

    if len(patient_ids) < 2:
        return {}, []

    model = AgglomerativeClustering(
        n_clusters=min(n_clusters, len(patient_ids)),
        metric="precomputed",
        linkage="average"
    )

    labels = model.fit_predict(distance_matrix)

    clusters = {}

    for pid, label in zip(patient_ids, labels):
        clusters.setdefault(label, []).append(pid)

    return clusters, labels



# =====================================================
# DBSCAN clustering
# =====================================================

def dbscan_clustering(
        distance_matrix,
        patient_ids,
        eps=100,
        min_samples=3):

    if len(patient_ids) < 2:
        return {}, []


    model = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="precomputed"
    )


    labels = model.fit_predict(distance_matrix)


    clusters = {}

    for pid, label in zip(patient_ids, labels):

        clusters.setdefault(label, []).append(pid)


    return clusters, labels