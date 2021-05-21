import re

class INCAR:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            incar = f.read()

        ispin_re = re.compile('ISPIN\W+(?P<ispin>\d)')
        ncl_re = re.compile('LNONCOLLINEAR\W+(?P<ncl>[a-zA-Z])')
        soc_re = re.compile('LSORBIT\W+(?P<ncl>[a-zA-Z])')
        proj_re = re.compile('LORBIT\W+(?P<lorbit>\d+)')
        m = ispin_re.search(incar)
        if m: 
            self.ispin = int( m.group('ispin') )
            self.ncl = False
        else:
            self.ispin = -1
            m = ncl_re.search( incar )
            if m: 
                tmp = m.group('ncl')
                print(tmp)
                if ( tmp == 'T' or tmp=='TRUE' ): self.ncl=True
            else:
                m = soc_re.search( incar )
                if m:
                    tmp = m.group('ncl')
                    if ( tmp == 'T' or tmp=='TRUE' ): self.ncl=True
                    else: self.ncl=False

        m = proj_re.search( incar )
        if m:
            self.lorbit = int( m.group('lorbit') )
        else: self.lorbit = -1

