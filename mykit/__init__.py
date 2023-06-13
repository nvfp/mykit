import os as _os
import pkg_resources as _pr


try:
    pkg = _pr.get_distribution('mykit')
except _pr.DistributionNotFound:
    ## This exception happens during GitHub Actions testing, let's handle it this way.
    class _Testing:
        version = 'testing'
        project_name = 'mykit'
    pkg = _Testing


__version__ = pkg.version


LIB_DIR_PTH = _os.path.dirname(_os.path.abspath(__file__))
LIB_NAME = pkg.project_name
