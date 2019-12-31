'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import os, sys


# load in dependencies dlls if on win

if sys.platform.startswith('win') :

    from ctypes import WinDLL

    dir_path = os.path.join( os.path.dirname(os.path.realpath(__file__)),

    for dependency in os.listdir( dir_path ) :
        
        if not dependency.endswith(".lib"):

            WinDLL( os.path.join( dir_path, dependency ) )


# export all edm functions

from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
