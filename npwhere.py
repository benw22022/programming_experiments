import numpy as np


if __name__ == "__main__":

    weights = np.arange(0, 10)
    labels = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 1])

    weights = np.where(labels != 0, weights, 1)

    print(weights)