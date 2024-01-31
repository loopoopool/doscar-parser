import sys
import numpy as np
from Ploos import Doscar as dos
from matplotlib import pyplot as plt
from matplotlib import rcParams

rcParams['axes.labelsize'] = 25
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['legend.fontsize'] = 20

labels = { 0 : '$d_{yz}$', 1 : '$d_{xz}$', 2 : '$d_{xy}$' }
orbtable = [ 'dyz', 'dxz', 'dx2'] 
colors = [ 'dodgerblue', 'forestgreen', 'crimson' ]

doscar = dos.DOSCAR('.')
atom = int( sys.argv[1] )
pb1 = doscar.projector([ atom ], [ 'dyztot' ])
pb2 = doscar.projector([ atom ], [ 'dxztot', 'dx2tot' ])

fig, ax = plt.subplots(figsize=(5,4.3))
ax.set_xlabel('$E-E_{F}$ (eV)')
ax.set_xlim(-0.5, 0.5)
ax.set_ylabel('states ($eV^{-1}$)')
ax.set_ylim(0, 7)
ax.set_yticks(range(8))

ax.plot(doscar.energy, doscar.dos, label='total', color='lightgrey')
ax.fill_between(doscar.energy, np.zeros(doscar.energy.shape), doscar.dos, color='lightgrey', alpha=0.6)
ax.plot(doscar.energy, pb1, label='PB1', color=colors[0])
ax.plot(doscar.energy, pb2, label='PB2', color=colors[2])
ax.axvline(x=0.0, color='black')

ax.legend(loc='best')
fig.tight_layout()
fig.savefig('singion.svg')

tmp = np.array( [doscar.energy, doscar.dos, pb1, pb2] )
np.save('dosplot.npy', tmp)
