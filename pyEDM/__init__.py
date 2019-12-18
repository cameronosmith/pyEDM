'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['PATH'] += ';'+dir_path
print(os.environ['PATH'])

from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
