from Parser import *

class CHGCAR:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.readlines()
        self.name = data[0]
        self.scalingFactor = float(remove_all_whitespace(data[1]))
        self.ucMatrix = self.scalingFactor * \
            np.array([extract_coord(line) for line in data[2:5]])
        self.atomsLabel = split(whitespace_to_semicol(data[5]))
        self.atomsNumber = [int(x)
                                for x in split(whitespace_to_semicol(data[6]))]
        self.ntot = sum(self.atomsNumber)
        self.selectiveDynamicsEnabled = re.compile(r'^[sS]')
        index = 7
        if self.selectiveDynamicsEnabled.match(data[index]):
            index = 8
            self.SelectiveDynamics = True
        else:
            self.SelectiveDynamics = False
        self.coorType = remove_all_whitespace(data[index])
        self.direct = (self.coorType == 'Direct' or self.coorType == 'direct' or
                   self.coorType == 'D' or self.coorType == 'd')
        index += 1
        if self.direct:
            self.directMatrix = np.array([extract_coord(line) for line in data[index:index+self.ntot]])
            self.cartesianMatrix = np.matmul(self.directMatrix, self.ucMatrix)
        else:
            self.cartesianMatrix = np.array([ extract_coord( line ) for line in data[index:index+self.ntot] ] )

        index += self.ntot+1
        self.nx, self.ny, self.nz = (int(x) for x in \
                split(whitespace_to_semicol(data[index])))
        ntot = self.nx*self.ny*self.nz
        nlines = int( ntot/5 )
        index += 1
        self.chgcar = np.array([ extract_coord( line ) for line in \
            data[index:index+nlines] ])
        self.chgcar = self.chgcar.reshape(ntot).reshape(self.nx, self.ny,
                self.nz)
        self.grid = np.array( [[[np.array([nx/self.nx, ny/self.ny,
            nz/self.nz]) @ self.ucMatrix for nz in range(self.nz)]
                for ny in range(self.ny)] for nx in range(self.nx)] )
        self.ChgcarCart = np.array( [[[ np.append(self.grid[nx, ny, nz], self.chgcar[nx, ny, nz]) for nx in range(self.nx) ] for ny in range(self.ny) ] for nz in
            range(self.nz) ] )
        print( 'done' )

