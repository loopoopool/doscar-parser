import numpy as np
from ploos import Eigenval
from matplotlib import pyplot as plt

k, e, o = Eigenval.loadEigenval('EIGENVAL')

nkxline = 20
nkpts = np.size(k,0)
x = np.zeros(nkpts)
for i, kk in enumerate(k):
    if i%nkxline == 0:
        k0 = kk
    x[i] = np.linalg.norm(kk-k0)
    for j in range(i): x[i] += x[j]

print(x)

