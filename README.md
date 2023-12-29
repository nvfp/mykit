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

Run `pip install -r requirements.txt` if you're using functions that need these dependencies.


## examples

```python
from mykit.kit.text import byteFmt
from mykit.app.arrow import Arrow
from mykit.app.slider import Slider

x = byteFmt(3141592653589793)
print(x)  # 2.79 PiB
```


## License

This project's source code and documentation are under the MIT license.
