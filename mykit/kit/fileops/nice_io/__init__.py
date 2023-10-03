## dev-docs: This is the variation and the next generation of mykit.kit.path.SafeJSON.
##           SafeJSON will be deprecated soon. TODO: Make NiceJSON, which is the next generation of it.

import json as _json
from typing import (
    Any as _Any,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union,
)

from mykit.kit.fileops.simple import (
    norm_pth as _norm_pth,
    dont_worry_the_path_ends_with as _dont_worry_the_path_ends_with,
    definitely_a_file as _definitely_a_file,
)


class NiceIO:
    """Procedurally strict for performing file operations like read, write, and rewrite."""

    @staticmethod
    def read(file_path:str, /, suffixes:_Optional[_Union[str, _Tuple[str, ...]]]=None) -> _Any:

        ## Normalize
        path_normalized = _norm_pth(file_path)

        ## Checks
        _definitely_a_file(path_normalized)
        _dont_worry_the_path_ends_with(path_normalized, suffixes)

        ## Read
        with open(path_normalized, 'r') as fp:
            out = _json.load(fp)
        
        return out

    @staticmethod
    def write(file_path:str, /):
        pass

    @staticmethod
    def rewrite(file_path:str, /):
        pass

    @staticmethod
    def recover(file_path:str, /):
        pass
