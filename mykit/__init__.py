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


LIB_REPO = 'https://github.com/nvfp/mykit'
LIB_NAME = 'mykit'
LIB_DIST_NAME = pkg.project_name  # distribution name

_ROOT_DIR_PTH = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # should only be used for development
DIST_DIR_PTH = _os.path.join(_ROOT_DIR_PTH, LIB_DIST_NAME)
# print(f'DEBUG: _ROOT_DIR_PTH = {_ROOT_DIR_PTH}')
# print(f'DEBUG: DIST_DIR_PTH = {DIST_DIR_PTH}')

APP_DIR_PTH = _os.path.join(DIST_DIR_PTH, 'app')
KIT_DIR_PTH = _os.path.join(DIST_DIR_PTH, 'kit')
REC_DIR_PTH = _os.path.join(DIST_DIR_PTH, 'rec')
WEB_DIR_PTH = _os.path.join(DIST_DIR_PTH, 'web')
# print(f'DEBUG: APP_DIR_PTH = {APP_DIR_PTH}')
