import numpy as np
import distancia
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from pcametric import PCAMetric


def CCS_metric(x, y):
    n_pts, n_dims = np.shape(x)
    return -np.sum(x * y) / n_pts


def SSE_metric(x, y):
    n_pts, n_dims = np.shape(x)
    return np.linalg.norm(x - y) ** 2 / n_pts


def COS_metric(x, y):
    sum = 0.0
    n_pts, n_dims = np.shape(x)
    for i in range(n_pts - 1):
        sum += (
            np.arccos(
                np.clip(
                    np.dot(x[i + 1] - x[i], y[i + 1] - y[i])
                    / (
                        np.linalg.norm(x[i + 1] - x[i])
                        * np.linalg.norm(y[i + 1] - y[i])
                    ),
                    -1,
                    1,
                )
            )
            / np.pi
        )
    return sum / n_pts


# def Pearson_metric(x, y):
#     n_pts, n_dims = np.shape(x)
#     pearson_dist = distancia.Pearson()
#     dist = 0
#     for dim in range(n_dims):
#         dist += pearson_dist.calculate(x[:, dim], y[:, dim])
#     return dist/n_dims


def Pearson_metric(x, y):
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    y_scaled = scaler.fit_transform(y)
    pca = PCA(n_components=1)
    x_pca = pca.fit_transform(x_scaled).squeeze()
    y_pca = pca.fit_transform(y_scaled).squeeze()
    pearson_dist = distancia.Pearson()
    dist = pearson_dist.calculate(x_pca, y_pca)
    return dist


def PCA_metric(x, y):
    # Setting parameters
    num_components = 1
    normalization = "precise"
    preprocess = "std"
    result, _, _ = PCAMetric(x, y, num_components, normalization, preprocess)
    edv, ad = result["exp_var_diff"], result["comp_angle_diff"]
    return ad
