import numpy as np
from scipy.stats import poisson

mu = 3
rv = poisson(mu)

x = np.arange(rv.ppf(0.0001), rv.ppf(0.9999))

for item in x:
    print(f'x: {item} -> {rv.pmf(item)}')