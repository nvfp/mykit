## dev-docs: This is the variation and the next generation of mykit.kit.path.SafeJSON.
##           SafeJSON will be deprecated soon. TODO: Make NiceJSON, which is the next generation of it.

import json as _json
import os as _os
from typing import (
    Any as _Any,
)

from mykit.kit.fileops.simple import (
    norm_pth as _norm_pth,
    dont_worry_the_path_ends_with as _dont_worry_the_path_ends_with,
    definitely_a_file as _definitely_a_file,
    definitely_a_dir as _definitely_a_dir,
    this_path_must_not_exist as _this_path_must_not_exist
)


class NiceJSON:
    """Procedurally strict for performing file operations like read, write, and rewrite"""

    @staticmethod
    def read(file_path:str, /) -> _Any:
        """
        Get the content of the given JSON file path

        ## Exceptions
        - Please manually inspect this function for all possible exceptions
        """

        ## Normalize
        path_normalized = _norm_pth(file_path)

        ## Checks
        _definitely_a_file(path_normalized)
        _dont_worry_the_path_ends_with(path_normalized, '.json')

        ## Read
        with open(path_normalized, 'r') as fp:
            out = _json.load(fp)
        
        return out

    @staticmethod
    def write(file_path:str, content:_Any) -> None:
        """
        Write the given `content` into a new JSON file

        ## Exceptions
        - Please manually inspect this function for all possible exceptions
        """

        ## Normalize
        path_normalized = _norm_pth(file_path)

        ## Checks
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        _definitely_a_dir(_os.path.dirname(path_normalized))
        _this_path_must_not_exist(path_normalized)

        with open(path_normalized, 'w') as fp:
            _json.dump(content, fp)

    @staticmethod
    def rewrite(file_path:str, content:_Any) -> None:
        """
        Replace the existing JSON file at `file_path` with the new `content`

        ## Exceptions
        - Please manually inspect this function for all possible exceptions
        """

        ## Normalize
        path_normalized = _norm_pth(file_path)

        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'

        ## Checks
        _dont_worry_the_path_ends_with(path_normalized, '.json')
        _definitely_a_file(path_normalized)
        _this_path_must_not_exist(tmp_path)
        _this_path_must_not_exist(bak_path)

        ## Run
        with open(tmp_path, 'w') as fp: _json.dump(content, fp)  # writing the new as temp
        _os.rename(path_normalized, bak_path)                    # backup the previous
        _os.rename(tmp_path, path_normalized)                    # rename the temp to the new
        _os.remove(bak_path)                                     # delete the previous

    @staticmethod
    def recover(file_path:str, /) -> None:
        """
        Try to fix the broken JSON file, mostly because of interrupted or sudden
        stops when performing `NiceJSON.rewrite` above. Note that this is still
        not fully optimized and might still change in the future.

        ## Exceptions
        - Please manually inspect this function for all possible exceptions
        """

        ## Normalize
        path_normalized = _norm_pth(file_path)

        tmp_path = path_normalized + '.tmp'
        bak_path = path_normalized + '.bak'

        ## Checks
        _dont_worry_the_path_ends_with(path_normalized, '.json')


        ## case I
        if _os.path.exists(path_normalized) and _os.path.exists(tmp_path) and (not _os.path.exists(bak_path)):
            _os.remove(tmp_path)
            return

        ## case II
        if (not _os.path.exists(path_normalized)) and _os.path.exists(tmp_path) and _os.path.exists(bak_path):
            _os.rename(tmp_path, path_normalized)
            _os.remove(bak_path)
            return

        ## case III
        if _os.path.exists(path_normalized) and (not _os.path.exists(tmp_path)) and _os.path.exists(bak_path):
            _os.remove(bak_path)
            return

        ## case IV (weirdly happening, but currently disabled because i dont know if this is also happening on different environments)
        # if (not _os.path.exists(path_normalized)) and (not _os.path.exists(tmp_path)) and _os.path.exists(bak_path):
        #     _os.rename(bak_path, path_normalized)
        #     return
