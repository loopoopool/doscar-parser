import sys
import numpy as np
from ploos import Poscar as p

psym = p.POSCAR( sys.argv[1] )
pcar = p.POSCAR( sys.argv[2] )

delta = pcar.cartesianMatrix - psym.cartesianMatrix

a = 1.0
b = 30.0

poxNew = (a-b)*psym.cartesianMatrix + b*pcar.cartesianMatrix
lc = np.linalg.norm( psym.ucMatrix[0] )

tmp={}
coo={}
squares = { 'square1' : ['13_1', '15_2', '16_4', '14_5'],
        'square2' : ['14_1', '16_2', '15_4', '13_5'],
        'square3' : ['16_1', '14_2', '13_4', '15_5'],
        'square4' : ['15_1', '13_2', '14_4', '16_5'],
        'square5' : ['16_1', '16_2', '16_4', '16_5'] }

for key in squares: tmp[key] = ''

for os in range(13,17):
    for nn, i in enumerate(pcar.octahedron( os )):
        if nn != 2 and nn != 5:
            x = poxNew[i-1][0]
            y = poxNew[i-1][1]
            label = str(os)+'_'+str(nn+1)
#            tmp[label] = '        \\node[draw,circle,fill=red] at ({:.7f}, '.format(x)
            tmp[label] = '        \\draw[fill=Crimson] ({:.7f}, '.format(x) 
            tmp[label] += '{:.7f}'.format(y)
#            tmp[label] += ') {}; % ' + label + '\n'
            tmp[label] += ') circle[radius=7pt]; % ' + label + '\n'
            coo[label] = ' ({:.7f}, '.format(x)
            coo[label] += '{:.7f}'.format(y) + ') '

for key in squares:
    tmp[key] = '        \\draw'
    for label in squares[key]:
        tmp[key] += coo[label] + '--'
    tmp[key] += coo[squares[key][0]] + ';\n'

tex='\\documentclass{standalone}\n'\
'\\usepackage[svgnames]{xcolor}\n'\
'\\usepackage{tikz}\n'\
'\\usetikzlibrary{calc, angles}\n'\
'\\usepackage{ifthen}\n'\
'\\newcommand\\lc{' + str(lc) + '}\n'\
'\n\\begin{document}\n'\
'\n\\begin{tikzpicture}\n'\
'	\\foreach \\x in {0,0.5,1}{\n'\
'		\\foreach \\y in {0,0.5,1}{\n'\
'			\\draw[fill=Peru] ($(\\x*\\lc, \\y*\lc)$) circle[radius=12pt];\n'\
'			\\node at ($(\\x*\\lc, \\y*\lc)$) {Os};\n'\
'		}\n'\
'	}\n'
for key in tmp:
    tex += tmp[key]

tex+='\\end{tikzpicture}\n\\end{document}'


with open('000jt.tex', 'w') as f:
    f.write(tex)

