import numpy as np
import similaritymeasures


def CCS_metric(x, y):
    return -np.sum(x * y)


def SSE_metric(x, y):
    return np.linalg.norm(x - y) ** 2


def COS_metric(x, y):
    sum = 0.0
    n_pts, n_dims = np.shape(x)
    for i in range(n_pts - 1):
        sum += (
            np.arccos(
                np.dot(x[i + 1] - x[i], y[i + 1] - y[i])
                / (np.linalg.norm(x[i + 1] - x[i]) * np.linalg.norm(y[i + 1] - y[i]))
            )
            / np.pi
        )
    return sum / (n_pts - 1)


def START_metric(x, y):
    return np.linalg.norm(x[0, :] - y[0, :])


def END_metric(x, y):
    return np.linalg.norm(x[-1, :] - y[-1, :])


def PCM_metric(x, y):
    return similaritymeasures.pcm(x, y)


def AREA_metric(x, y):
    return similaritymeasures.area_between_two_curves(x, y)


def FRECHET_metric(x, y):
    return similaritymeasures.frechet_dist(x, y)


def CRVLEN_metric(x, y):
    return similaritymeasures.curve_length_measure(x, y)


def DTW_metric(x, y):
    dtw, d = similaritymeasures.dtw(x, y)
    return dtw


def MAE_metric(x, y):
    return similaritymeasures.mae(x, y)


def MSE_metric(x, y):
    return similaritymeasures.mse(x, y)
