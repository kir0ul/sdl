import numpy as np


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
