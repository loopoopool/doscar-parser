import sys
import numpy as np
from Ploos import Doscar as dos
from matplotlib import pyplot as plt

labels = { 0 : '$d_{yz}$', 1 : '$d_{xz}$', 2 : '$d_{x^2-y^2}$',
    3 : '$d_{z^2}$', 4 : '$d_{xy}$' }
orbtable = [ 'dyz', 'dxz', 'dx2', 'dz2', 'dxy' ] 
colors = [ 'dodgerblue', 'forestgreen', 'crimson' ]

doscar = dos.DOSCAR('.')
#atom = int( sys.argv[1] )
#orbital = sys.argv[2]
offset = 13
fig = plt.figure(figsize=(8.268,11.693), constrained_layout=True)
fig.suptitle('Plane 1', fontsize='xx-large')
subfigs = fig.subfigures(nrows=4, ncols=1)
for row, subfig in enumerate(subfigs):
    atom = row + offset
    subfig.supylabel('Os-' + str(atom) + ' states ($eV^{-1}$)')
    axs = subfig.subplots(nrows=1, ncols=3, sharey=True)
    for col, ax in enumerate(axs):
        if row == 0:
            ax.set_title(labels[col], fontsize='x-large', color=colors[col])
        ax.set_xlim(min(doscar.energy), max(doscar.energy))
        ax.set_ylim(0, 3)
        ax.set_yticks(range(4))
        ax.plot(doscar.energy, doscar.dos, label='total', color='lightgrey')
        ax.fill_between(doscar.energy, np.zeros(doscar.energy.shape), doscar.dos, color='lightgrey', alpha=0.6)
        ax.plot(doscar.energy, doscar.projector([ atom ], [ orbtable[col]+'tot' ]),
                label=labels[col], color=colors[col])
        ax.axvline(x=0.0, color='black')
#        ax.legend(loc='upper right')
#        ax.legend(loc='upper right', prop={'size' : 30})
#fig, axes = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True,
#        figsize=(38,36))

#offset=9
#for i, ax in enumerate(axes.flatten()):
#    if i%3 == 0: orbital='dyz'
#    if i%3 == 1: orbital='dxz'
#    if i%3 == 2: orbital='dx2'
#    if i/3<1 : atom=offset
#    elif i/3<2 : atom=offset+1
#    elif i/3<3 : atom=offset+2
#    else : atom=offset+3
#    ax.set_xlim(min(doscar.energy), max(doscar.energy))
#    ax.set_ylim(0, 3)
#    ax.set_yticks(range(4))
#    ax.tick_params(labelsize=25)
#    ax.plot(doscar.energy, doscar.dos, label='total', color='lightgrey')
#    ax.fill_between(doscar.energy, np.zeros(doscar.energy.shape), doscar.dos, color='lightgrey', alpha=0.6)
#    ax.plot(doscar.energy, doscar.projector([atom], [orbital+'tot']),
#            label=labels[orbital])
#    ax.axvline(x=0.0, color='black')
#    ax.legend(loc='upper right', prop={'size' : 20})

#fig.supxlabel('$E-E_{F}$ (eV)', fontsize=30)
fig.supxlabel('$E-E_{F}$ (eV)')
fig.savefig('plane1.png')

