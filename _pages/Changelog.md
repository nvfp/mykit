---
layout: main
title: Changelog
permalink: /changelog
redirect_from:
  - /changelog/
---

# Changelog


- 9.0.0 (Aug 7, 2023):
    - Breaking changes:
        - The `bg` arg for `.kit.color.Colored` is now optional. Note that this breaking change propagates to all functions that are using `Colored`.
    - Added `num_round` to `.kit.text`, and its unit test.
    - Added `.ghactions` master module.
    - Added `TimeFmt` to `.kit.time`.

- 
<!-- The hyphen '-' above so that the 9.0.0 release (via fast-pypi-release) doesn't contain these comments -->
<!-- Note: 8.1.0 has been aborted, but 8.1.0b1 published on PyPI -->
~~- 8.1.0 (Aug 7, 2023):~~
~~    - Added `num_round` to `.kit.text`, and its unit test.~~
~~    - Added `.ghactions` master module.~~
- 8.0.0 (Aug 6, 2023):
    - Breaking changes:
        - Now, `.kit.utils.merge_dicts` will preserve both input dictionaries (the input dicts remain intact).
    - Added `merging_dicts` and `add_dict_val` to `.kit.utils`, and their unit tests.

- 7.1.0 (Aug 6, 2023):
    - Added `merge_dicts` to `.kit.utils`, and its unit test.
- 7.0.0 (Aug 6):
    - Breaking changes:
        - Updated default `gap` value in `.kit.text.num_approx` function from 1 to 0.
    - Added `sort_dict_by_key`, `sort_dict_by_val`, `get_first_n_dict_items`, `get_last_n_dict_items`, `randhex`, and `reverse_dict` to `.kit.utils`

- 6.2.0 (Aug 2):
    - Added `num_approx` to `mykit.kit.text`, including its unit tests.
- 6.1.0 (Aug 2):
    - Added `in_byte` and `connum` to `mykit.kit.text`, including their unit tests.
    - Added `hex_to_rgb`, `Hex`, and `Colored` to `mykit.kit.color`, including some unit tests.
    - Added `mykit.kit.pLog`.
- 6.0.0 (July 5):
    - Breaking changes:
        - The `component` now requires the `app: App` argument as a positional argument in the `.app.App.after_initialization_use` method
- 5.3.0 (July 4):
    - Added `.app.App.after_initialization_use` and `.app.App.add_dependencies` methods
- 5.2.0 (July 4):
    - The `.kit.keycrate` now accepts tuple of strings as arguments for both `only_keys` and `need_keys`
- 5.1.0 (July 3):
    - Added `dependencies` arg to `.app.App.use`
- 5.0.0 (July 2):
    - Breaking changes:
        - Removed `architecture` arg from `.app.App`
    - Tweaking `.app.App` and `.app.architecture.Eventdriven`
    - Deleted `/app/architecture/__init__.py`
- 4.1.0 (June 21, 2023):
    - NEW: in `/kit/utils.py`: `slowprint` and `print_screen`
- 4.0.0 (June 18, 2023):
    - Breaking changes:
        - `LIB_DIR_PTH` in `mykit` replaced by `DIST_DIR_PTH`
        - Changed `/app/` mechanism:
            - removed `/app/_runtime.py`
    - `.app.App.listen`: Added aliases for event listener types
    - New: `/app/architecture`
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