import re
import numpy as np

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
