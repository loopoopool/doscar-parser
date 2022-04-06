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
