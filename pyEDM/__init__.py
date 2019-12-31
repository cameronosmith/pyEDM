'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import os, sys


# load in dependencies dlls if on win

if sys.platform.startswith('win') :

    import numpy


# export all edm functions

from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
