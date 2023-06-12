# myKit

[![pypi version](https://img.shields.io/pypi/v/mykit?logo=pypi)](https://pypi.org/project/mykit/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

Python utility toolkit.


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

- 1.0.0 (June 12, 2023):
    - `kit/quick_visual/plot2d.py`: changed argument name: `graph2d_cfg` -> `cfg`
- 0.1.3 (June 12, 2023):
    - removed `get_gray` from `mykit/mykit/kit/color.py`
    - transform `mykit/mykit/kit/gui/button/` -> `mykit/mykit/app/button.py`
    - transform `mykit/mykit/kit/gui/label/` -> `mykit/mykit/app/label.py`
    - transform `mykit/mykit/kit/gui/slider/` -> `mykit/mykit/app/slider.py`
    - transform `mykit/mykit/kit/gui/shape/` -> `mykit/mykit/app/arrow.py`
    - transform `mykit/mykit/kit/neuralnet/dense/` -> `mykit/mykit/kit/neuralnet/dense.py`
    - transform `mykit/mykit/kit/neuralnet/genetic/` -> `mykit/mykit/kit/neuralnet/genetic.py`
- 0.1.0 (June 12, 2023):
    - migrated all modules from [carbon](https://github.com/nvfp/carbon) into `mykit/mykit/kit/`
    - deleted `mykit/mykit/kit/math/`
    - added `mykit/mykit/rec/` and `mykit/mykit/app/`
    - transform `mykit/mykit/kit/color/` -> `mykit/mykit/kit/color.py`
    - moved `mykit/mykit/kit/color/test_color.py` to `mykit/tests/test_kit/test_color.py`
    - transform `mykit/mykit/kit/ffmpeg/` -> `mykit/mykit/kit/ffmpeg.py`
    - deleted `mykit/mykit/kit/graph/graph2d/`
    - transform `mykit/mykit/kit/graph/graph2d/v2.py` -> `mykit/mykit/kit/graph/graph2d.py`
    - transform `mykit/mykit/kit/maths/` -> `mykit/mykit/kit/math.py`
    - moved `mykit/mykit/kit/maths/test_maths.py` -> `mykit/tests/test_math.py`
    - transform `mykit/mykit/kit/noise/` -> `mykit/mykit/kit/noise.py`
    - transform `mykit/mykit/kit/path/` -> `mykit/mykit/kit/path.py`
    - transform `mykit/mykit/kit/text/` -> `mykit/mykit/kit/text.py`
    - transform `mykit/mykit/kit/time/` -> `mykit/mykit/kit/time.py`
    - transform `mykit/mykit/kit/utils/` -> `mykit/mykit/kit/utils.py`


## Troubleshoot

- To report bugs/issues or ask questions, you can reach me [here](https://nvfp.github.io/contact) or open an issue/pull request.


## License

This project is licensed under the MIT license.