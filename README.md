# myKit🧰

[![Run tests](https://github.com/nvfp/mykit/actions/workflows/run-tests.yml/badge.svg)](https://github.com/nvfp/mykit/actions/workflows/run-tests.yml)
[![Rebuild docs](https://github.com/nvfp/mykit/actions/workflows/rebuild-docs.yml/badge.svg)](https://github.com/nvfp/mykit/actions/workflows/rebuild-docs.yml)
[![pypi version](https://img.shields.io/pypi/v/mykit?logo=pypi)](https://pypi.org/project/mykit/)

Collections of common functions for Python.

![banner](_etc/assets/banner.jpg)

[Documentation](https://nvfp.github.io/mykit)


## Usage

```sh
pip install mykit
```


## examples

```python
from mykit.kit.text import byteFmt
from mykit.app.arrow import Arrow
from mykit.app.slider import Slider

x = byteFmt(3141592653589793)
print(x)  # 2.79 PiB
```


## Dependencies

Install these if you're using functions that need these dependencies.

- `numba>=0.55.2`
- `numpy>=1.22.4`


## License

[MIT License](https://en.wikipedia.org/wiki/MIT_License). Everyone is welcome to share, alter, contribute, sell, etc. the code.
