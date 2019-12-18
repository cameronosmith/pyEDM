'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import os, ctypes
dir_path = os.path.dirname(os.path.realpath(__file__))
ctypes.WinDLL(dir_path+os.path.sep+"libopenblas.dll")

from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
