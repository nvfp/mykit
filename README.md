# myKit

This is a Python toolkit that bundles handy utility functions such as color interpolations, activation functions, Perlin noise, and others. The aim is to build them from the ground up to help understand how they work.

*Quick Tip*: If you're here because you need to run a specific project that uses this module, you can jump directly to the **Installation** section.

![carbon's banner](_archive/20230515-banner-640.jpg)


## Installation

- Manual:

    1. Download the latest [version](https://github.com/nvfp/carbon/releases)
    2. Remove the version number (`carbon-1.x.x` -> `carbon`)
    3. Place it in a folder where Python can recognize it as a module (e.g. `~/code/carbon`)
    4. Install dependencies:

        - libraries:

            ```sh
            pip install -r /path/to/carbon/requirements.txt
            ```

            or navigate to the `carbon` folder:

            ```sh
            pip install -r requirements.txt
            ```
        - [FFmpeg](https://ffmpeg.org/download.html) (optional, if the project needs it. Any version should be okay, but version 5 or latest is recommended)


## Usage

- check the version:

    ```sh
    python carbon -v
    ```

- Basic:

    ```python
    from carbon.ffmpeg import get_audio_sample_rate
    from carbon.gui.button import Button
    from carbon.time import get_sexagecimal
    from carbon.utils import minmax_normalization
    ```

- Testing:

    ```sh
    python -m unittest
    ```

    ```sh
    python carbon\_testing\noise#__init__.py#perlin_noise_1d.py
    ```


## Compatibility purposes

TL;DR: It's recommended to always use the latest version.

Sometimes, when I need to add a feature or make big changes, I find starting over is the least stressful way to ensure older projects don't break. Here's how I manage the generations across the module.

**Minor** (argument order, scaling, generalization, etc.):
- `carbon.mdl.fn` -> `carbon.mdl.fn2`
- `carbon.mdl.fn` -> `carbon.mdl.v2.fn`

**Major** (data structure, component relations, overall usage, etc.):
- `carbon.mdl.Class` -> `carbon.mdl_v2.Class`
- `carbon.module` -> `carbon.module_new_name`

Mostly, basic functions (standalone, input-in-output-out) are the ones that undergo **Minor** changes. **Major** changes are mostly expected in structured things like big modules (interconnected functions, specific usage rules).


## FAQ

- About this module:


- Compatibility:

    Latest version is always compatible with older versions (e.g., `carbon-1.3.0` works with projects that use `carbon-1.0.0` or `carbon-1.2.0`)


## Changelog

- 0.1.3 (June 12, 2023):
    -
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

- If Python can't find the module, as indicated by `ModuleNotFoundError: No module named 'carbon'`, try putting it in Python's standard folder for external libraries (`~/Python3/Lib/site-packages`).
- To report bugs/issues or ask questions, you can reach me [here](https://nvfp.github.io/contact) or open an issue/pull request.


## License

This project is licensed under the MIT license.