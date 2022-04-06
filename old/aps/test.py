import Doscar
import numpy as np
from matplotlib import pyplot as plt

pristine = Doscar.DOSCAR('.')

#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
fig = plt.figure(figsize=(9,8))
gs = fig.add_gridspec(2, hspace=0.1)
(ax1, ax2) = gs.subplots(sharex=True, sharey=True)

ax1.plot(pristine.energy, pristine.dos, label='total', color='lightgrey')
ax1.axvline(x=0.0, color='black', label='fermi')
ax1.fill_between(pristine.energy, np.zeros(pristine.energy.shape), pristine.dos, color='lightgrey', alpha=0.6)
ax1.set_xlim(-0.7, 0.6)
ax1.set_ylim(0, 30)
ax1.tick_params(labelsize=20)
ax1.label_outer()

plt.show()
