import re
import numpy as np
from ploos.Parser import *

class BandStructure:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.readlines()
        
        for i, line in enumerate(data):
            if (re.search('E-fermi', line)) : 
                m = re.match('.*?(E-fermi).*?(-?[0-9]+[.][0-9]+)', line)
                self.ef = float( m.group(2) )
                print('@ line : ', i, ' E-fermi : ', self.ef)
                break

        for i, line in enumerate(data):
            if (re.search('NKPTS', line)) : 
                m = re.match('.*?(NKPTS)\s+\=\s+([0-9]+).*?NBANDS.*?([0-9]+)$', line)
                self.nkpts = int( m.group(2) )
                self.nbands = int( m.group(3))
                print('@ line : ', i, ' nkpts : ', self.nkpts, ' nbands : ',
                        self.nbands)
                break
       
        self.nkseg = 0
        for i, line in enumerate(data):
            if (re.search('^\s+Generated.*?points', line)) : 
                m = re.match('^\s+Generated\s+([0-9]+)\s+points', line)
                self.nkseg = int( m.group(1) )
                print('Each k-point segment contains ', self.nkseg, ' points.')
                break

        self.kpath = np.zeros((self.nkpts, 4))

        ibeg=0
        for i, line in enumerate(data):
            m = re.search(r'2pi/SCALE', line)
            if (re.search('2pi/SCALE', line)): 
                ibeg = i
                break

        for i in range(self.nkpts):
            self.kpath[i] = extract_coord(data[ibeg+i+1])[1]

        self.bands = np.zeros((self.nkpts, self.nbands))
        for i, line in enumerate(data[ibeg+self.nkpts:]):
            m = re.match('^.*?k-point\s+([0-9]+).*?(\s+[0-9]\.[0-9]+){3}$', line)
            if m: 
                nk = int(m.group(1))-1
                if (nk > self.nkpts): break
                ibbeg = ibeg+self.nkpts+i+2
                for ib in range(self.nbands):
#                    print( data[ibbeg+ib] )
                    self.bands[nk,ib] = extract_coord(data[ibbeg+ib])[0][1]


    def plot_data(self):
        nseg = int(self.nkpts/self.nkseg)
        print( nseg )
        xdim = self.nkpts - nseg + 1
        xarr = np.zeros(xdim)
        yarr = np.zeros((xdim, self.nbands))
        offset = 0.0
        shift = 0
        k0 = self.kpath[0,:-1]
        print( k0 )
        self.hspp = np.zeros(nseg+1)
        ihsp = 0
        for i, k in enumerate(self.kpath[:,:-1]):
            if i%self.nkseg != 0 or i==0:
                xarr[i-shift] = np.linalg.norm(k-k0) + offset
                yarr[i-shift] = self.bands[i]
                if (self.nkpts-i-1)%self.nkseg==0:
                    k0 = k
                    offset = xarr[i-shift]
                    ihsp += 1
                    self.hspp[ihsp] = offset
            else: shift += 1

        return xarr, yarr
