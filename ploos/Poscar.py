import sys
import re
import itertools
import numpy as np
from ploos.Parser import *

eps = 1e-3


def pbc(x):
    for i in range(len(x)):
        if x[i] > 1.0:
            x[i] -= 1.0
        elif x[i] < 0.0: x[i] += 1.0
        if abs(x[i]-1) < eps:
            x[i] = 0.0
    return x


def octa(x, os):
    for i, xi in enumerate(x):
        if xi - os[i] > 0.5:
            x[i] -= 1.0
        elif xi - os[i] < -0.5: x[i] += 1.0
    return x


class POSCAR:
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

    def write_to_file(self, coordinate, filename):
        data = [self.name ]
        data.append(str( self.scalingFactor ) + '\n' )
        for i in range(np.size( self.ucMatrix, 0 ) ):
            data.append( '    {0:>13.11f}  {1:>13.11f}  {2:>13.11f}\n'.format(self.ucMatrix[i, 0], self.ucMatrix[i,1], self.ucMatrix[i,2]) )
        labels = '   '
        for lab in self.atomsLabel:
            labels += lab + '  '
        data.append( labels + '\n' )
        labels = '   '
        for lab in self.atomsNumber:
            labels += str(lab) + '  '
        data.append( labels + '\n' )
        if self.SelectiveDynamics :
            data.append( 'Selective Dynamics\n' )
        data.append( self.coorType + '\n' )
        if np.size(coordinate, 0 ) != self.ntot:
            raise Exception('Wrong number of atoms.')
        if np.size(coordinate, 1 ) != 3:
            raise Exception('Wrong number of coordinates.')
        for i in range(self.ntot ):
            data.append( '{0:>13.11f}  {1:>13.11f}  {2:>13.11f}\n'.format(coordinate[i, 0], coordinate[i,1], coordinate[i,2]) )
        with open(filename, 'w') as f:
            f.writelines(data )

    def getCartesianCoordinates(self, atomNumber):
        return self.cartesianMatrix[atomNumber-1]

    def getDirection(self, atom1, atom2):
        d = self.cartesianMatrix[atom2-1] - self.cartesianMatrix[atom1-1]
        return d/np.linalg.norm(d)

    def getBondLength(self, atom1, atom2):
        c1 = self.cartesianMatrix[atom1-1]
        c2 = self.cartesianMatrix[atom2-1]
        d = np.array([min( [abs(c2[i] - c1[i]), abs(c2[i] - c1[i] -
                                                     np.linalg.norm(self.ucMatrix[i])), abs(c2[i] - c1[i] +
                                                   np.linalg.norm(self.ucMatrix[i]))]) for i in range(3)] )
        return np.linalg.norm(d)

    def getNN(self, atom, num):
        d = {i+1: self.getBondLength(i+1, atom) for i in range(self.ntot)}
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        return dict(itertools.islice(d.items(), 1, num+1))

    def octahedron(self, atom):
        nn = self.getNN(atom, 6)
        print(nn)
        c1 = pbc(self.directMatrix[atom-1])
        ordered_nn = {}
        for nnkey in nn:
            c2 = octa(pbc(self.directMatrix[nnkey-1]), c1)
            d = c2 - c1
            print(d)
            d /= np.linalg.norm(d)
            if d[0] > 0. and abs(d[1]) < eps and abs(d[2]) < eps:
                ordered_nn.update({1: nnkey})
            elif abs(d[0]) < eps and d[1] > 0. and abs(d[2]) < eps:
                ordered_nn.update({2: nnkey})
            elif d[0] < 0. and abs(d[1]) < eps and abs(d[2]) < eps:
                ordered_nn.update({4: nnkey})
            elif abs(d[0]) < eps and d[1] < 0. and abs(d[2]) < eps:
                ordered_nn.update({5: nnkey})
            elif d[2] > 0.:
                ordered_nn.update({3: nnkey})
            elif d[2] < 0.:
                ordered_nn.update({6: nnkey})
                # rotated cell
#            if d[0] > 0. and d[1] > 0. and abs(d[2]) < eps:
#                ordered_nn.update({1: nnkey})
#            elif d[0] < 0. and d[1] > 0. and abs(d[2]) < eps:
#                ordered_nn.update({2: nnkey})
#            elif d[0] < 0. and d[1] < 0. and abs(d[2]) < eps:
#                ordered_nn.update({4: nnkey})
#            elif d[0] > 0. and d[1] < 0. and abs(d[2]) < eps:
#                ordered_nn.update({5: nnkey})
#            elif d[2] > 0.:
#                ordered_nn.update({3: nnkey})
#            elif d[2] < 0.:
#                ordered_nn.update({6: nnkey})
        ordered_nn = {k: v for k, v in sorted(ordered_nn.items(), key=lambda item: item[0])}
        return [ordered_nn[key] for key in ordered_nn]
