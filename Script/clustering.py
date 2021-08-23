from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def PCA_values(df, columns, scaler, n_components=2):
    # Filtrar columnas
    X       = df.filter(columns).reset_index().drop("registro_id", axis=1)
    # Ajustar y transformar los datos, incluir valores a un dataframe
    columns_scaled = [col+"_scaled" for col in columns]
    X_scaled       = pd.DataFrame(scaler.fit_transform(X), columns = columns_scaled)
    
    # Análisis de componentes principales para n_componentes
    pca = PCA(n_components=n_components)
    pca = pd.DataFrame(pca.fit_transform(X_scaled), columns = ["pca 1", "pca 2"])
    
    new_df = pd.concat([X, X_scaled, pca], axis=1)
    return new_df


from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.metrics import silhouette_score

def Elbow_Method(data, n_clusters, columns, **kwargs):
    sse = []
    data = data.filter(columns)
    for k in n_clusters:
        kmeans_model = KMeans(n_clusters=k, random_state=42)
        kmeans_model.fit(data)
        sse.append(kmeans_model.inertia_)

    kl = KneeLocator(
        n_clusters, sse, curve="convex", direction="decreasing"
    )
    fig, ax = plt.subplots(figsize = (12, 6))
    ax.plot(n_clusters, sse, 'bo-')
    ax.set_xlabel('n_clusters')
    ax.set_ylabel('SSE')
    ax.set_title('The Elbow Method plot (k ideal = '+str(kl.elbow)+')')
    return

def Silhouette_Coefficient_kmeans(data, n_clusters, columns, **kwargs):
    # n_clusters >= 2
    silhouette_coefficients = []
    data = data.filter(columns)
    
    for k in n_clusters:
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(data)
        score = silhouette_score(data, model.labels_, random_state=42)
        silhouette_coefficients.append(score)

    fig, ax = plt.subplots(figsize = (12, 6))
    ax.plot(n_clusters, silhouette_coefficients, 'bo-')
    ax.set_xlabel('n_clusters')
    ax.set_ylabel("Silhouette Coefficient")
    ax.set_title('Silhouette Coefficients plot')
    return

from sklearn.cluster import DBSCAN

def Silhouette_Coefficient_DBSCAN(data, columns, parameters, **kwargs):
    silhouette_coefficients = []
    data_filter = data.filter(columns)
    
    for eps in parameters["eps"]:
        for min_samples in parameters["min_samples"]:
            dbscan = DBSCAN(eps = eps, min_samples = min_samples)
            preds  = dbscan.fit_predict(data_filter)
            if np.unique(preds)[0] == -1:
                pass
            else:
                score  = silhouette_score(data_filter, preds)
                silhouette_coefficients.append([eps, min_samples, score])
    silhouette_coefficients = pd.DataFrame(silhouette_coefficients, columns = ["eps","min_samples","score"])
    return silhouette_coefficients.sort_values("score", ascending=False)

import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import AgglomerativeClustering

def Silhouette_Coefficient_sch(data, n_clusters, columns, **kwargs):
    # n_clusters >= 2
    silhouette_coefficients = []
    data = data.filter(columns)
    
    for k in n_clusters:
        sch_model = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='complete')
        sch_model.fit(data)
        score = silhouette_score(data, sch_model.labels_, random_state=42)
        silhouette_coefficients.append(score)

    fig, ax = plt.subplots(figsize = (12, 6))
    ax.plot(n_clusters, silhouette_coefficients, 'bo-')
    ax.set_xlabel('n_clusters')
    ax.set_ylabel("Silhouette Coefficient")
    ax.set_title('Silhouette Coefficients plot')
    return