'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import os
from ctypes import WinDLL
dir_path = os.path.dirname(os.path.realpath(__file__))
os.listdir(".")
WinDLL("libopenblas.dll")

from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
