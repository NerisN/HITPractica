import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering, AffinityPropagation
from sklearn.metrics import silhouette_score, davies_bouldin_score

def prepare_data(data: list) -> np.ndarray:
    """Preprocesa datos aplicando Z-score normalization."""
    if not data or len(data) < 3:
        return None

    df = pd.DataFrame(data)
    features = df[['co2_ppm', 'temperatura']].values

    scaler = StandardScaler()
    features_normalized = scaler.fit_transform(features)

    return features_normalized

def apply_gmm(data: np.ndarray, n_clusters: int = 4) -> dict:
    """Aplica Gaussian Mixture Models para clustering."""
    if data is None or len(data) < n_clusters:
        return {"error": "Datos insuficientes para GMM"}

    try:
        gmm = GaussianMixture(n_components=n_clusters, random_state=42)
        labels = gmm.fit_predict(data)

        silhouette = silhouette_score(data, labels)
        davies_bouldin = davies_bouldin_score(data, labels)

        return {
            "algoritmo": "GMM",
            "clusteres": int(n_clusters),
            "labels": labels.tolist(),
            "silhouette_score": float(silhouette),
            "davies_bouldin_score": float(davies_bouldin),
            "medias": gmm.means_.tolist()
        }
    except Exception as e:
        return {"error": str(e)}

def apply_spectral(data: np.ndarray, n_clusters: int = 4) -> dict:
    """Aplica Spectral Clustering."""
    if data is None or len(data) < n_clusters:
        return {"error": "Datos insuficientes para Spectral Clustering"}

    try:
        spectral = SpectralClustering(n_clusters=n_clusters, random_state=42, affinity='rbf')
        labels = spectral.fit_predict(data)

        silhouette = silhouette_score(data, labels)
        davies_bouldin = davies_bouldin_score(data, labels)

        return {
            "algoritmo": "Spectral Clustering",
            "clusteres": int(n_clusters),
            "labels": labels.tolist(),
            "silhouette_score": float(silhouette),
            "davies_bouldin_score": float(davies_bouldin)
        }
    except Exception as e:
        return {"error": str(e)}

def apply_affinity_propagation(data: np.ndarray) -> dict:
    """Aplica Affinity Propagation (descubre K automáticamente)."""
    if data is None or len(data) < 3:
        return {"error": "Datos insuficientes para Affinity Propagation"}

    try:
        ap = AffinityPropagation(random_state=42, preference=-50)
        labels = ap.fit_predict(data)
        n_clusters = len(np.unique(labels))

        silhouette = silhouette_score(data, labels)
        davies_bouldin = davies_bouldin_score(data, labels)

        return {
            "algoritmo": "Affinity Propagation",
            "clusteres": int(n_clusters),
            "labels": labels.tolist(),
            "silhouette_score": float(silhouette),
            "davies_bouldin_score": float(davies_bouldin)
        }
    except Exception as e:
        return {"error": str(e)}

def run_clustering_analysis(data: list) -> dict:
    """Ejecuta análisis de clustering con los 3 algoritmos."""
    if not data:
        return {"error": "No hay datos para analizar"}

    prepared_data = prepare_data(data)

    if prepared_data is None:
        return {"error": "No se pudo preparar los datos"}

    results = {
        "total_registros": len(data),
        "algoritmos": []
    }

    results["algoritmos"].append(apply_gmm(prepared_data))
    results["algoritmos"].append(apply_spectral(prepared_data))
    results["algoritmos"].append(apply_affinity_propagation(prepared_data))

    return results
