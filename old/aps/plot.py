import Doscar
import numpy as np
from matplotlib import pyplot as plt

pristine = Doscar.DOSCAR('pristine')
polaron = Doscar.DOSCAR('polaron')

#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, sharey=True)
fig = plt.figure(figsize=(9,8))
gs = fig.add_gridspec(2, hspace=0.1)
(ax1, ax2) = gs.subplots(sharex=True, sharey=True)

ax1.plot(pristine.energy, pristine.dos, label='total', color='lightgrey')
ax1.fill_between(pristine.energy, np.zeros(pristine.energy.shape), pristine.dos, color='lightgrey', alpha=0.6)
ax1.axvline(x=0.0, color='black', label='fermi')
ax1.set_xlim(-0.7, 0.6)
ax1.set_ylim(0, 30)
ax1.tick_params(labelsize=20)
ax1.label_outer()

ax2.plot(polaron.energy, polaron.dos, label='total', color='lightgrey')
ax2.fill_between(polaron.energy, np.zeros(polaron.energy.shape), polaron.dos, color='lightgrey', alpha=0.6)
pole = np.array([x for x in polaron.energy if x > -0.2 and x < 0.0])
poldos = np.array([x for i, x in enumerate(polaron.dos) if polaron.energy[i] >
    -0.2 and polaron.energy[i] < 0.0 ])
ax2.fill_between(pole, np.zeros(pole.shape), poldos,
        color='gold', alpha=0.6)
ax2.plot(polaron.energy, polaron.projector([16], ['dxztot', 'dyztot', 'dx2tot']),
    label='Os ($t_{2g}$)', color='blue')
ax2.plot(polaron.energy, polaron.projector([34, 35, 38, 39, 42, 44], ['pxtot', 'pytot', 'pztot']),
    label='O (p)', color='red', linestyle='dashed')
ax2.axvline(x=0.0, color='black')
ax2.set_xlim(-0.7, 0.6)
ax2.set_ylim(0, 30)
ax2.tick_params(labelsize=20)
ax2.label_outer()

fig.supxlabel('$E-E_{F}$ (eV)', size=25)
fig.supylabel('states ($eV^{-1}$)', size=25)

handles, labels = ax2.get_legend_handles_labels()
fig.legend(handles, labels,bbox_to_anchor=(0.9, 0.89), loc='upper right', prop={'size' : 20})

plt.show()
