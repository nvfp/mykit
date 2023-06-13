# myKit

Python utility toolkit.

![mykit's banner](assets/20230613-mykit-banner-fhd.png)

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

- 1.1.0 (June 13, 2023):
    - NEW: `app/__init__.py`
- 1.0.0 (June 12, 2023):
    - changed arg name: `kit/quick_visual/plot2d.py`: `graph2d_cfg` -> `cfg`
- 0.1.3 (June 12, 2023):
    - removed `get_gray` from `kit/color.py`
    - transform `kit/gui/button/` -> `app/button.py`
    - transform `kit/gui/label/` -> `app/label.py`
    - transform `kit/gui/slider/` -> `app/slider.py`
    - transform `kit/gui/shape/` -> `app/arrow.py`
    - transform `kit/neuralnet/dense/` -> `kit/neuralnet/dense.py`
    - transform `kit/neuralnet/genetic/` -> `kit/neuralnet/genetic.py`
- 0.1.0 (June 12, 2023):
    - migrated all modules from [carbon](https://github.com/nvfp/carbon) into `kit/`
    - deleted `kit/math/`
    - added `rec/` and `app/`
    - transform `kit/color/` -> `kit/color.py`
    - moved `kit/color/test_color.py` to `mykit/tests/test_kit/test_color.py`
    - transform `kit/ffmpeg/` -> `kit/ffmpeg.py`
    - deleted `kit/graph/graph2d/`
    - transform `kit/graph/graph2d/v2.py` -> `kit/graph/graph2d.py`
    - transform `kit/maths/` -> `kit/math.py`
    - moved `kit/maths/test_maths.py` -> `mykit/tests/test_math.py`
    - transform `kit/noise/` -> `kit/noise.py`
    - transform `kit/path/` -> `kit/path.py`
    - transform `kit/text/` -> `kit/text.py`
    - transform `kit/time/` -> `kit/time.py`
    - transform `kit/utils/` -> `kit/utils.py`


## Troubleshoot

- To report bugs, please open an issue/pull request, or you can reach me [here](https://nvfp.github.io/contact).


## License

This project is licensed under the MIT license.
