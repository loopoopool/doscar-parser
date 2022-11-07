import re
import numpy as np
from ploos.Parser import *
from ploos.Kpoints import loadKpath as lK


class EIGENVAL:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.readlines()
        tmp = whitespace_to_semicol(data[5])
        nbands = int(split(tmp)[-1])
        nkpts = int(split(tmp)[-2])
        off = 7
        self.e = np.zeros((nkpts,nbands))
        self.k = np.zeros((nkpts,3))
        self.o = np.zeros((nkpts,nbands))
        for i in range(nkpts):
            self.k[i] = extract_coord(data[off+i*(2+nbands)])[0]
            for j in range(1,nbands+1):
                tmp = split(data[off+i*(2+nbands)+j])
                self.e[i,j-1] = float(tmp[1])
                self.o[i,j-1] = float(tmp[2])
        self.nbands = nbands
        self.nkpts = nkpts

    def preparePlot(self, kfilename):
        self.xticks_labels, self.nkxline = lK(kfilename)
        nseg = int(self.nkpts/self.nkxline)
        xdim = self.nkpts - nseg + +1
        self.x = np.zeros(xdim)
        self.y = np.zeros((self.nbands, xdim))
        k0 = self.k[0]
        offset = 0.0
        shift = 0
        self.xticks_pos = [0.]
        for i, kk in enumerate(self.k):
            if i%self.nkxline != 0 or i==0:
                self.x[i-shift] = np.linalg.norm(kk-k0) + offset
                self.y[:,i-shift] = self.e[i]
                if (self.nkpts-i-1)%self.nkxline == 0: 
                    k0 = kk
                    offset = self.x[i-shift]
                    self.xticks_pos.append(self.x[i-shift])
            else: 
                shift += 1

    def getZero(self, bandindex=-1):
        # calculate Valence Band Maximum
        tmp = 0.0
        itmp = 0
        jtmp = 0
        otmp = 0.0
        for i, ok in enumerate(self.o):
            for j, oo in enumerate(ok):
                if oo >= otmp and j > jtmp:
                    jtmp = j
                    otmp = oo
            if self.e[i,jtmp] > tmp: 
                tmp = self.e[i,jtmp]
        self.vbm = tmp
        if bandindex > -1:
            tmp = max(self.e[:,bandindex-1])
        return tmp

