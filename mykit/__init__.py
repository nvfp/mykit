import os
import pkg_resources


__version__ = pkg_resources.get_distribution('mykit').version


LIB_DIR_PTH = os.path.dirname(os.path.abspath(__file__))
LIB_NAME = os.path.basename(LIB_DIR_PTH)
