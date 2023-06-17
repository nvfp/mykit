# myKit

Python utility toolkit.

The aim of this project is to understand how things work by building them from the ground up, while also providing a lightweight version of something that already exists out there.

<!-- reminder: use this link (don't use relative path to the one in the repo) to be able to display the banner on PyPI -->
![mykit's banner](https://raw.githubusercontent.com/nvfp/mykit/master/assets/20230613-mykit-banner-fhd.png)

[![pypi version](https://img.shields.io/pypi/v/mykit?logo=pypi)](https://pypi.org/project/mykit/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)


## Installation

```sh
pip install mykit
```


## Usage

```python
from mykit.kit.text import byteFmt
from mykit.app.arrow import Arrow
from mykit.app.slider import Slider


x = byteFmt(3141592653589793)
print(x)  # 2.79 PiB
```


## FAQ

- 


## Changelog

- 3.0.0 (June 17, 2023):
    - Breaking changes:
        - Changed `title` arg to `name` in `.app.App`
        - Now `/kit/keycrate` must be a .txt file, and the file must exist
        - Added `export` method to `.kit.keycrate.KeyCrate`
    - Added test suite for `.kit.keycrate.KeyCrate`
- 2.0.4 (June 16, 2023):
    - Now `move` method of `Button`, `Label`, and `_Slider` will return self
- 2.0.3 (June 16, 2023):
    - Now `.app.complex.plot.Plot` and `.app.complex.plot.Biplot` can be used even if no points is specified
    - Added `add_background_processes` to `.app.App`
- 2.0.2 (June 14, 2023):
    - finished updating all type hints
    - Added visibility functionality to `/app/complex/plot.py`
- 2.0.1 (June 14, 2023):
    - Updated all type hints to make them work on Python 3.8 and 3.9
    - Added visibility functionality to `/app/complex/biplot.py`
- 2.0.0 (June 13, 2023):
    - Breaking changes:
        - New mechanism for app: `/app/__init__.py`
        - Moved: `/kit/graph/graph2d.py` -> `/app/complex/plot.py`
        - transform: `/kit/quick_visual/plot2d.py` -> `/kit/fast_visualizations/static/plot.py`
    - Bugfixed:
        - folder `mykit/tests/` should also be excluded during build (rc version)
    - New: `/app/complex/biplot.py`
- 1.0.0 (June 12, 2023):
    - changed arg name: `/kit/quick_visual/plot2d.py`: `graph2d_cfg` -> `cfg`
- 0.1.3 (June 12, 2023):
    - removed `get_gray` from `/kit/color.py`
    - transform `/kit/gui/button/` -> `/app/button.py`
    - transform `/kit/gui/label/` -> `/app/label.py`
    - transform `/kit/gui/slider/` -> `/app/slider.py`
    - transform `/kit/gui/shape/` -> `/app/arrow.py`
    - transform `/kit/neuralnet/dense/` -> `/kit/neuralnet/dense.py`
    - transform `/kit/neuralnet/genetic/` -> `/kit/neuralnet/genetic.py`
- 0.1.0 (June 12, 2023):
    - migrated all modules from [carbon](https://github.com/nvfp/carbon) into `/kit/`
    - deleted `/kit/math/`
    - added `/rec/` and `/app/`
    - transform `/kit/color/` -> `/kit/color.py`
    - moved `/kit/color/test_color.py` to `mykit/tests/test_kit/test_color.py`
    - transform `/kit/ffmpeg/` -> `/kit/ffmpeg.py`
    - deleted `/kit/graph/graph2d/`
    - transform `/kit/graph/graph2d/v2.py` -> `/kit/graph/graph2d.py`
    - transform `/kit/maths/` -> `/kit/math.py`
    - moved `/kit/maths/test_maths.py` -> `mykit/tests/test_math.py`
    - transform `/kit/noise/` -> `/kit/noise.py`
    - transform `/kit/path/` -> `/kit/path.py`
    - transform `/kit/text/` -> `/kit/text.py`
    - transform `/kit/time/` -> `/kit/time.py`
    - transform `/kit/utils/` -> `/kit/utils.py`


## Troubleshoot

- To report bugs, please open an issue/pull request, or you can reach me [here](https://nvfp.github.io/contact).


## License

This project is licensed under the MIT license.
