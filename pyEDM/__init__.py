'''Python interface to cppEDM github.com/SugiharaLab/cppEDM'''

import os

import glob
basedir = os.path.dirname(__file__)
for filename in glob.glob(os.path.join(basedir,'*openblas*dll')):
    print(os.path.abspath(filename),flush=True)
    from ctypes import WinDLL
    WinDLL(os.path.abspath(filename))


from pyEDM.CoreEDM import *
from pyEDM.AuxFunc import *
