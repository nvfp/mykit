import os as _os
import pkg_resources as _pr


__version__ = _pr.get_distribution('mykit').version


LIB_DIR_PTH = _os.path.dirname(_os.path.abspath(__file__))
LIB_NAME = _pr.get_distribution('mykit').project_name
