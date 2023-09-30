## dev-docs: This is the variation and the next generation of mykit.kit.path.SafeJSON.
##           SafeJSON will be deprecated soon. TODO: Make NiceJSON, which is the next generation of it.

from typing import (
    Any as _Any,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union,
)


class NiceIO:
    """Procedurally strict for performing file operations like read, write, and rewrite."""

    @staticmethod
    def read(file_path:str, /, suffixes:_Optional[_Union[str, _Tuple[str, ...]]]=None) -> _Any:
        pass

    @staticmethod
    def write(file_path:str, /):
        pass

    @staticmethod
    def rewrite(file_path:str, /):
        pass

    @staticmethod
    def recover(file_path:str, /):
        pass
