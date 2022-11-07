import re
import numpy as np
from itertools import groupby
from ploos.Parser import *

def loadKpath(filename):
    with open(filename, 'r') as f:
        data = f.readlines()

    tmp = whitespace_to_semicol(data[1])
    nkpts_xline = int( tmp.split(';')[0] )
    count = 0
    hskpt = []
    backslash = re.compile(r'\\')
    beg = re.compile(r'^')
    end = re.compile(r'$')
    for line in data[4:]:
        if remove_all_whitespace(line) != '':
            count += 1
            tmp = whitespace_to_semicol(line)
            tmp = split(tmp)[-1]
            tmp = re.sub(beg, '$', tmp)
            hskpt.append(re.sub(end, '$', tmp))
    hskpt = [ x[0] for x in groupby(hskpt) ]
    return hskpt, nkpts_xline


def loadKpathFromOutcar(filename):
    with open(filename, 'r') as f:
        data = f.readlines()

    for i, line in enumerate(data):
        if (re.search('NKPTS', line)) : 
            m = re.match('.*?(NKPTS)\s+\=\s+([0-9]+).*?NBANDS.*?([0-9]+)$', line)
            print(m)
            nkpts = int( m.group(2) )
            nbands = int( m.group(3))
            print('@ line : ', i, ' nkpts : ', nkpts, ' nbands : ', nbands)
            break

    kpath = np.zeros((nkpts, 4))

    ibeg=0
    for i, line in enumerate(data):
        m = re.search(r'2pi/SCALE', line)
        if (re.search('2pi/SCALE', line)): 
            ibeg = i
            break

    for i in range(nkpts):
        kpath[i] = extract_coord(data[ibeg+i+1])

    print( kpath )

    bands = np.zeros((nkpts, nbands))
    for i, line in enumerate(data[ibeg+nkpts:]):
        m = re.match('^.*?k-point\s+([0-9]+).*?(\s+[0-9]\.[0-9]+){3}$', line)
        if m: 
            nk = int(m.group(1))-1
            if (nk > nkpts): break
            ibbeg = ibeg+nkpts+i+2
            for ib in range(nbands):
                bands[nk,ib] = extract_coord(data[ibbeg+ib])[1]

    print( bands[0,:] )

