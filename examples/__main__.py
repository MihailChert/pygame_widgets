import sys
import os
import importlib

from lib import *


if len(sys.argv) > 0 and os.path.isfile(sys.path[0] + f'{os.path.sep}examples{os.path.sep}{sys.argv[1]}.py'):
    importlib.import_module('examples.' + sys.argv[1])
    # print(sys.argv)
else:
    raise RuntimeError(f'Unknown python file with name {sys.argv[1]}')
