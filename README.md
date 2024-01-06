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

- numba>=0.55.2
- numpy>=1.22.4


## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

###### *Everyone is welcome to open, read, modify, contribute, share, reuse, whatever for good humankind purposes. You are awesome, and have a great day!*
