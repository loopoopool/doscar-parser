import re

class INCAR:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            incar = f.read()

        ispin_re = re.compile('ISPIN\W+(?P<ispin>\d)')
        ncl_re = re.compile('LNONCOLLINEAR\W+(?P<ncl>[a-zA-Z])')
        soc_re = re.compile('LSORBIT\W+(?P<ncl>[a-zA-Z])')
        proj_re = re.compile('LORBIT\W+(?P<lorbit>\d+)')
        mincar = ispin_re.search(incar)
        mncl = ncl_re.search( incar )
        msoc = soc_re.search( incar )
        
        if mincar: 
            self.ispin = int( m.group('ispin') )
            self.ncl = False
        elif mncl:
            self.ispin=-1
            tmp = mncl.group('ncl')
            if ( tmp == 'T' or tmp=='TRUE' ): 
                self.ncl=True
            else:
                exit('Failed to parse INCAR')
        elif msoc:
            self.ispin=-1
            tmp = msoc.group('ncl')
            if ( tmp == 'T' or tmp=='TRUE' ): self.ncl=True
            else:
                exit('Failed to parse INCAR')
        else: 
            self.ncl=False
            self.ispin=1

        m = proj_re.search( incar )
        if m:
            self.lorbit = int( m.group('lorbit') )
        else: self.lorbit = -1

