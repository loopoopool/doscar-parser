import re
import numpy as np
from Ploos import Parser

def loadEigenval(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    
    tmp = remove_all_whitespace(data[6])
    print(tmp)

loadEigenval('EIGENVAL')
