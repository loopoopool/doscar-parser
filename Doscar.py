import sys, re, Incar, PlotGUI
import numpy as np
from PyQt5.QtWidgets import QApplication

label_ispin1 = [ 's', 'p', 'd']
label_ispin1_lm = [ 's', 'px', 'py', 'pz', 'dxy', 'dyz', 'dz2', 'dxz', 'dx2' ]
label_ispin2 = [ 's+', 's-', 'p+', 'p-', 'd+', 'd-' ]
label_ispin2_lm = [ 's+', 'px+', 'py+', 'pz+', 'dxy+', 'dyz+', 'dz2+', 'dxz+', 'dx2+', 
        's-', 'px-', 'py-', 'pz-', 'dxy-', 'dyz-', 'dz2-', 'dxz-', 'dx2-' ]
label_ncl = [ 'stot' , 's(mx)', 's(my)', 's(mz)', 'ptot', 'p(mx)', 'p(my)', 'p(mz)', 
        'dtot', 'd(mx)', 'd(my)', 'd(mz)' ]
label_ncl_lm = [ 'stot', 's(mx)', 's(my)', 's(mz)', 'pxtot', 'px(mx)', 'px(my)', 'px(mz)', 
        'pytot', 'py(mx)', 'py(my)', 'py(mz)', 'pztot', 'pz(mx)', 'pz(my)', 'pz(mz)', 
        'dxytot', 'dxy(mx)', 'dxy(my)', 'dxy(mz)', 'dyztot', 'dyz(mx)', 'dyz(my)', 'dyz(mz)',
        'dz2tot', 'dz2(mx)', 'dz2(my)', 'dz2(mz)', 'dxztot', 'dxz(mx)', 'dxz(my)', 'dxz(mz)',
        'dx2tot', 'dx2(mx)', 'dx2(my)', 'dx2(mz)' ]

def remove_all_whitespace(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', x)

def whitespace_to_semicol(x):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, ';', x)

def split(x):
    return whitespace_to_semicol( x ).split( ';' )[1:-1]

def extract_coord(x):
    coo = whitespace_to_semicol( x ).split( ';' )[1:4]
    return np.array( [float(ci) for ci in coo] )

def parse_yn_bool(x):
    if ( x == 'y' ): 
        return True
    elif ( x == 'n' ): 
        return False
    else:
        print('\n!!!!! Invalid Answer - Aborting !!!!!\n')
        exit(-1)

# discarding energy column
# l=0 lm=f ncl=f isp=1 ncol=1
# l=0 lm=f ncl=f isp=2 ncol=2
# l=0 lm=f ncl=t       ncol=3
# l=0 lm=t ncl=f isp=1 ncol=1
# l=0 lm=t ncl=f isp=2 ncol=2
# l=0 lm=t ncl=t       ncol=3
# l=1 lm=f ncl=f isp=1 ncol=2
# l=1 lm=f ncl=f isp=2 ncol=4
# l=1 lm=f ncl=t       ncol=6
# l=1 lm=t ncl=f isp=1 ncol=4
# l=1 lm=t ncl=f isp=2 ncol=8
# l=1 lm=t ncl=t       ncol=17
# l=2 lm=f ncl=f isp=1 ncol=4
# l=2 lm=f ncl=f isp=2 ncol=8
# l=2 lm=f ncl=t       ncol=15
# l=2 lm=t ncl=f isp=1 ncol=9
# l=2 lm=t ncl=f isp=2 ncol=18
# l=2 lm=t ncl=t       ncol=38

def todic(labelarray):
    return { x : i for i, x in enumerate(labelarray) }



class DOSCAR:
    ##### COSNTRUCTOR #####
    def __init__(self):
        pass

    def __init__(self, path):
        incar = Incar.INCAR( path+'/INCAR' )
#        ispin=0
#        ncl = parse_yn_bool( input('Non-collinear?(y/n): ') )
#        if not ncl: ispin = int( input('ISPIN >> ') )
#        lm = parse_yn_bool( input('lm-decomposed dos?(y/n): ') )
        with open( path+'/DOSCAR', 'r' ) as f:
            doscar = f.readlines()

        self.natoms, _, pdos, _ = [int(n) for n in split( doscar[0] )]
        vol, a, b, c, potim = [float(n) for n in split( doscar[1] )]
        tebeg = float( remove_all_whitespace( doscar[2] ) )
        system = remove_all_whitespace( doscar[4] )
        emax, emin, nedos, efermi, _ = [float(n) for n in split( doscar[5] )]
        self.nedos = int(nedos)
        self.enableProjector = len(doscar) > self.nedos+7
        counter = 6
        self.energy = np.zeros(self.nedos)

        if ( incar.ispin != 2 ):
            self.dos = np.zeros(self.nedos)
            for i in range(self.nedos):
                self.energy[i], self.dos[i], _ = (float(x) for x in split( doscar[counter+i] ))
        else:
            self.dos_up = np.zeros(self.nedos)
            self.dos_down = np.zeros(self.nedos)
            for i in range(self.nedos):
                self.energy[i], self.dos_up[i], self.dos_down[i], _ = (float(x) for x in split( doscar[counter+i] ))

        self.energy -= efermi

        if ( self.enableProjector ):
            counter += self.nedos
            # skip header
            counter += 1
            ncol = len( split( doscar[self.nedos+7] ) ) - 1 # remove one col for energies
            self.pldos = np.zeros((self.natoms, self.nedos, ncol))

            for i in range(self.natoms):
                for j in range(self.nedos):
                    self.pldos[i,j] = np.array( [float(x) for x in split( doscar[counter] )[1:] ] )
                    counter += 1
                # skip header
                counter += 1

            # Extract labels
            lm = incar.lorbit == 11 or incar.lorbit == 1
            global label_ispin1_lm, label_ispin1, label_ispin2_lm, label_ispin2, label_ncl_lm, label_ncl
            if ( incar.ispin==1 ):
                if ( lm ): self.guiLabel = label_ispin1_lm[:ncol] 
                else: self.guiLabel = label_ispin1[:ncol]
            elif ( incar.ispin==2 ):
                if ( lm ): self.guiLabel = label_ispin1_lm[:ncol]
                else: self.guiLabel = label_ispin2[:ncol]
            elif ( incar.ncl ):
                if ( lm ): 
                    self.guiLabel = label_ncl_lm[:ncol]
                else: self.guiLabel = label_ncl[:ncol]
            else: exit('\nUnrecognised structure. Aborting...\n')
            self.label = todic( self.guiLabel )
    ##############################  

    ##### PROJECTOR #####
    def projector(self, atoms, orbitals):
        projected = np.zeros(self.nedos)
        for aa in atoms:
            for oo in orbitals:
                projected += self.pldos[ aa, :, self.label[oo] ]
        return projected
    ############################## 

    ##### PLOTTER #####
    def plot(self):
        app = QApplication(sys.argv)
        form = PlotGUI.App(self)
        form.show()
        app.exec_()
        #interface.app.exec_()
        #plt.plot(self.energy, self.dos, label='total')
        #plt.legend(loc='best')
        #plt.show()
