# myKit🧰

[![Run tests](https://github.com/nvfp/mykit/actions/workflows/run-tests.yml/badge.svg)](https://github.com/nvfp/mykit/actions/workflows/run-tests.yml)
[![pypi version](https://img.shields.io/pypi/v/mykit?logo=pypi)](https://pypi.org/project/mykit/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

Collections of common functions that can be reused. The idea is, let's try to understand how it works by remaking it. It's messy, but it works. Written in Python for Python projects.

![mykit's banner](https://raw.githubusercontent.com/nvfp/mykit/master/_etc/assets/banner.jpg)


## Installation

```sh
pip install mykit
```

If you use a module requiring these dependencies, run `pip install -r requirements.txt`.


## Give it a try!

```python
from mykit.kit.text import byteFmt
from mykit.app.arrow import Arrow
from mykit.app.slider import Slider

x = byteFmt(3141592653589793)
print(x)  # 2.79 PiB
```


## Misc

- [Thank you💙](https://nvfp.github.io/thank-you)
- [Documentation](https://nvfp.github.io/mykit)
- [Changelog](https://nvfp.github.io/mykit/changelog)


## License

This project's source code and documentation are under the MIT license.
