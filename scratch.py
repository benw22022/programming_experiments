import math
import numpy as np

def quadrature_errors(errors):
    return np.sqrt(np.sum(errors**2))

arr = np.linspace(0.001, 2, 8)

print(quadrature_errors(arr))