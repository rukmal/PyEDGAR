import os
import sys

try:
    import PyEDGAR
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath('../'))
    os.chdir(os.path.abspath('../'))
    import PyEDGAR
