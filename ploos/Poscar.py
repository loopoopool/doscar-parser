import sys
import re
import itertools
import numpy as np
from ploos.Parser import *

def pbc(x):
    eps = 1e-4
    for i in range(len(x)):
        if x[i] - 1.0 > eps:
            x[i] -= 1.0
        elif x[i] < -eps: x[i] += 1.0
        if abs(x[i]-1) < eps:
            x[i] = 0.0
    return x

def octa(x, os):
    for i, xi in enumerate(x):
        if xi - os[i] > 0.5:
            x[i] -= 1.0
        elif xi - os[i] < -0.5: x[i] += 1.0
    return x

class POSCAR(object):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.readlines()
        self.name = data[0]
        self.scalingFactor = float(remove_all_whitespace(data[1]))
        self.uc_print = np.array([extract_coord(line)[0] for line in data[2:5]])
        self.ucMatrix = self.scalingFactor * self.uc_print
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
        self.header = ''
        for i in range(index): self.header += data[i]
        self.headerLines = [x for x in data[:index]]
        self.SDflags = []
        tmpc_array = np.zeros( (self.ntot, 3) )
        if self.selectiveDynamicsEnabled:
            for i, line in enumerate(data[index:index+self.ntot]):
                tmpc, tmpf = extract_coord(line)
                tmpc_array[i] = tmpc
                self.SDflags.append( tmpf )
        else:
            tmpc_array = np.array([extract_coord(line)[0] for line in data[index:index+self.ntot]])
        if self.direct:
            self.directMatrix = tmpc_array
            self.cartesianMatrix = np.matmul(tmpc_array, self.ucMatrix)
        else:
            self.cartesianMatrix = tmpc_array
            self.directMatrix = np.matmul(tmpc_array, np.linalg.inv(self.ucMatrix))

    def _update_cartesianMatrix(self):
        tmp = np.array( [pbc(x) for x in self.directMatrix] )
        self.cartesianMatrix = np.matmul(tmp, self.ucMatrix)
    
    def _update_directMatrix(self):
        tmp = np.matmul(self.cartesianMatrix, np.linalg.inv(self.ucMatrix))
        self.directMatrix = np.array( [pbc(x) for x in tmp] )

    def write_to_file(self, filename, mode='D', digits=11):
        data = [self.name ]
        data.append(str( self.scalingFactor ) + '\n' )
        for i in range(np.size( self.uc_print, 0 ) ):
            data.append( '    {0:>13.11f}  {1:>13.11f} {2:>13.11f}\n'.format(self.uc_print[i, 0],
                                              self.uc_print[i,1], self.uc_print[i,2]) )
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
        data.append( mode + '\n' )
        tmp = []
        if (mode=='D'):
            self._update_directMatrix()
            for x, f in zip(np.round(self.directMatrix, digits), self.SDflags):
                tmp.append( (x[0], x[1], x[2], f[0], f[1], f[2]) )
        elif (mode=='C'):
            self._update_cartesianMatrix()
            for x, f in zip(np.round(self.cartesianMatrix, digits), self.SDflags):
                tmp.append( (x[0], x[1], x[2], f[0], f[1], f[2]) )
        else:
            raise Exception('Wrong mode.')
        
        for x in tmp:
            tmp_str = '  {0:>13.11f}  {1:>13.11f}  {2:>13.11f} {3:} {4:} {5:}\n'
            data.append( tmp_str.format(x[0], x[1], x[2], x[3], x[4], x[5]) )
        with open(filename, 'w') as f:
            f.writelines(data)

    def setCartesianCoordinates(self, atomNumber, vector):
        self.cartesianMatrix[atomNumber-1] = vector
        self._update_directMatrix()

    def getCartesianCoordinates(self, atomNumber):
        tmp = np.array( [x for x in self.cartesianMatrix[atomNumber-1]] )
        return tmp

    def getDirection(self, atom1, atom2):
        d = self.cartesianMatrix[atom2-1] - self.cartesianMatrix[atom1-1]
        return d/np.linalg.norm(d)

#    def getBondLength(self, atom1, atom2):
#        # prepare c1
#        c1 = self.cartesianMatrix[atom1-1]
#        print(c1)
#        tmp = np.dstack((c1,c1))
#        c1p = pbc(self.directMatrix[atom1-1]) @ self.ucMatrix
#        print(c1p)
#        tmp2 = np.dstack((c1p,c1p))
#        c1 = np.dstack((tmp,tmp2)).reshape((3,2,2))
#        # prepare c2
#        c2 = self.cartesianMatrix[atom2-1]
#        tmp = np.dstack((c2,c2))
#        c2p = pbc(self.directMatrix[atom2-1]) @ self.ucMatrix
#        tmp2 = np.dstack((c2p,c2p))
#        c2 = np.dstack((tmp,tmp2)).reshape((3,2,2))
#        # calculate
#        tmp = c1 - np.transpose(c2, axes=(0,2,1))
#        tmp = tmp.reshape((3,4))
#        tmp2 = np.array( [np.array([x, y, z]) for x in tmp[0] for y in tmp[1]
#            for z in tmp[2]]  )
#        tmp = np.array( [np.linalg.norm(x) for x in tmp2] )
#        print(tmp)
#        return np.min(tmp)

#    def _nn_helper(self, tmp, tmp2, cooArr):
#        x = np.append(cooArr, tmp.reshape((1,3)), axis=0)
#        y = np.append(tmp2, tmp.reshape((1,3)), axis=0)
#        return x, y

    def getBondLength(self, atom1, atom2):
        c1 = self.cartesianMatrix[atom1-1]
        c2 = self.cartesianMatrix[atom2-1]
        tmp = c1-c2
        tmp2 = tmp.reshape((1,3))
        for lv in self.ucMatrix:
            tmp = c1-c2-lv
            tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
            tmp = c1-c2+lv
            tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
        for lv in self.ucMatrix:
            for lv1 in self.ucMatrix:
                tmp = c1-c2-lv-lv1
                tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                tmp = c1-c2-lv+lv1
                tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                tmp = c1-c2+lv+lv1
                tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                tmp = c1-c2+lv-lv1
                tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
        for lv in self.ucMatrix:
            for lv1 in self.ucMatrix:
                for lv2 in self.ucMatrix:
                    tmp = c1-c2-lv-lv1-lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2-lv-lv1+lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2-lv+lv1-lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2-lv+lv1+lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2+lv+lv1-lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2+lv+lv1+lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2+lv-lv1-lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
                    tmp = c1-c2+lv-lv1+lv2
                    tmp2 = np.append(tmp2, tmp.reshape((1,3)), axis=0)
        tmp = np.array( [np.linalg.norm(x) for x in tmp2] )
        return np.min(tmp), tmp2[np.argmin(tmp)]

############ old ##################
#    def getBondLength(self, atom1, atom2):
#        c1 = self.cartesianMatrix[atom1-1]
#        c2 = self.cartesianMatrix[atom2-1]
#        d = np.array([min( [abs(c2[i] - c1[i]), abs(c2[i] - c1[i] -
#                                                     np.linalg.norm(self.ucMatrix[i])), abs(c2[i] - c1[i] +
#                                                   np.linalg.norm(self.ucMatrix[i]))]) for i in range(3)] )
#        return np.linalg.norm(d)
#####################################

    def getAngle(self, at1, at2, at3):
        vref = self.cartesianMatrix[at2-1]
        v1 = self.getBondLength(at1, at2)[1] - vref
        v1 /= np.linalg.norm(v1)
        v2 = self.getBondLength(at3, at2)[1] - vref
        v2 /= np.linalg.norm(v2)
        return 180./np.pi*np.arccos(np.dot(v1,v2))

    def getNN(self, atom, num):
        d = {i+1: self.getBondLength(i+1, atom)[0] for i in range(self.ntot)}
        d = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
        return dict(itertools.islice(d.items(), 1, num+1))

    def octahedron(self, atom):
        nn = self.getNN(atom, 6)
#        print(nn)
#        c1 = pbc(self.directMatrix[atom-1])
        ordered_nn = {}
        for nnkey in nn:
            d = self.getBondLength(nnkey, atom)[1]
#            c2 = octa(pbc(self.directMatrix[nnkey-1]), c1)
#            d = c2 - c1
#            print(d)
#            d /= np.linalg.norm(d)
            eps = 0.1*np.linalg.norm(d)
            if d[0] > 0. and d[1] > 0. and abs(d[2]) < eps:
                ordered_nn.update({1: nnkey})
            elif d[0] < 0. and d[1] > 0. and abs(d[2]) < eps:
                ordered_nn.update({2: nnkey})
            elif d[0] < 0. and d[1] < 0. and abs(d[2]) < eps:
                ordered_nn.update({4: nnkey})
            elif d[0] > 0. and d[1] < 0. and abs(d[2]) < eps:
                ordered_nn.update({5: nnkey})
            elif d[2] > 0.:
                ordered_nn.update({3: nnkey})
            elif d[2] < 0.:
                ordered_nn.update({6: nnkey})
        ordered_nn = {k: v for k, v in sorted(ordered_nn.items(), key=lambda item: item[0])}
        return [ordered_nn[key] for key in ordered_nn]
    
    def octahedron_cubic(self, atom):
        nn = self.getNN(atom, 6)
        ordered_nn = {}
        for nnkey in nn:
            d = self.getBondLength(nnkey, atom)[1]
#            c2 = octa(pbc(self.directMatrix[nnkey-1]), c1)
#            d = c2 - c1
#            print(d)
#            d /= np.linalg.norm(d)
            eps = 0.1*np.linalg.norm(d)
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
        ordered_nn = {k: v for k, v in sorted(ordered_nn.items(), key=lambda item: item[0])}
        return [ordered_nn[key] for key in ordered_nn]
    
    def octahedron_general(self, atom, x=np.array([1,0,0]), y=np.array([0,1,0]),
                           z=np.array([0,0,1])):
        nn = self.getNN(atom, 6)
        ordered_nn = {}
        d = { nnkey : self.getBondLength(nnkey, atom)[1] for nnkey in nn }
        d_from_x = { nnkey : np.linalg.norm( d[nnkey] - x *
                        np.inner(d[nnkey], x)) for nnkey in nn }
        d_from_x = [key for key, v in sorted(d_from_x.items(), key = lambda it :
                                             it[1])[:4]]
        
        d_from_y = { nnkey : np.linalg.norm( d[nnkey] - y *
                        np.inner(d[nnkey], y)) for nnkey in nn }
        d_from_y = [key for key, v in sorted(d_from_y.items(), key = lambda it :
                                             it[1])[:4]]
        
        d_from_z = { nnkey : np.linalg.norm( d[nnkey] - z *
                        np.inner(d[nnkey], z)) for nnkey in nn }
        d_from_z = [key for key, v in sorted(d_from_z.items(), key = lambda it :
                                             it[1])[:2]]

        for nnkey in d_from_x:
            if ( np.inner(d[nnkey], x) > 0.0 and np.inner(d[nnkey], y) >= 0.0):
                ordered_nn.update( {1: nnkey} )
            elif( np.inner(d[nnkey], x) < 0.0 and np.inner(d[nnkey], y) <= 0.0):
                ordered_nn.update( {4: nnkey} )
        
        for nnkey in d_from_y:
            if ( np.inner(d[nnkey], y) > 0.0 and np.inner(d[nnkey], x) <= 0.0):
                ordered_nn.update( {2: nnkey} )
            elif( np.inner(d[nnkey], y) < 0.0 and np.inner(d[nnkey], x) >= 0.0):
                ordered_nn.update( {5: nnkey} )
        
        for nnkey in d_from_z:
            if ( np.inner(d[nnkey], z) > 0.0 ):
                ordered_nn.update( {3: nnkey} )
            else:
                ordered_nn.update( {6: nnkey} )
        
        ordered_nn = {k: v for k, v in sorted(ordered_nn.items(), key=lambda item: item[0])}
        return [ordered_nn[key] for key in ordered_nn]

    def isAtBorder(self, x, tol):
        if abs(x) < tol or abs(x-1) < tol: return 'F'
        else: return 'T'

    def selectiveDynamicsConstraintBorders(self, outfile):
        flags = [ [self.isAtBorder(x, 1e-5) for x in atom] for atom in self.directMatrix ]
        if self.SelectiveDynamics: 
            text = self.header
        else:
            text = ''
            for i in range(len(self.headerLines)-1): 
                text += self.headerLines[i]
            text += 'Selective Dynamics\n' + self.headerLines[-1]
        for atom, flag in zip(self.directMatrix, flags):
            text += '  %.11f  %.11f  %.11f  %c  %c  %c\n' % (atom[0], atom[1], atom[2], flag[0], flag[1], flag[2])
        with open(outfile, 'w') as f: f.write(text)

