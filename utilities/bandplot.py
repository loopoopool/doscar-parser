import sys
import numpy as np
from ploos import Eigenval
from ploos.Kpoints import loadKpath as lK
from matplotlib import pyplot as plt
from matplotlib import rcParams

# plotting
rcParams['axes.labelsize'] = 25
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['legend.fontsize'] = 20

fig = plt.figure(figsize=(5,4.3))
ax = fig.subplots(nrows=1, ncols=1)

eig = Eigenval.EIGENVAL( sys.argv[1] )
eig.preparePlot( sys.argv[2] )

#
ib_min=100
ib_max=384
kmax=4
x = eig.x[:kmax*eig.nkxline-kmax+1]
y = eig.y[ib_min:ib_max,:kmax*eig.nkxline-kmax+1]
xticks_pos = eig.xticks_pos[:kmax]
xticks_labels = eig.xticks_labels[:kmax]


ax.set_xlim(xticks_pos[0], xticks_pos[-1])
ax.set_xticks(xticks_pos)
ax.set_xticklabels(xticks_labels)
ax.set_ylabel('energy (eV)')
for hsk in xticks_pos:
    ax.axvline(x=hsk, color='lightgrey')

for band in y: ax.plot(x, band, color='black')
fig.tight_layout()
plt.show()
