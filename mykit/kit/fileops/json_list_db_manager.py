import os as _os
import time as _time
from typing import (
    Any as _Any,
    List as _List,
)

from mykit.kit.fileops.simple import (
    same_ext_for_all_dir_files as _same_ext_for_all_dir_files,
    list_dir as _list_dir
)
from mykit.kit.path import SafeJSON as _SafeJSON
from mykit.kit.time import TimeFmt as _TimeFmt


class JsonListDbManager:
    """
    A simple database system that uses JSON file to store data as a list

    ---

    ## Demo
    
    The database folder:
    ```
    ## Note: the actual name would be `db_YYYYMMDD_HHMMSS.json`; below is just for conciseness.
    container/
    ├── db_1.json
    └── db_2.json
    ```
    
    The database file (`container/db_2.json`):
    ```
    ['x1', 'x2', 'and so on..']
    ```
    
    Let's say the latest database file (`db_2.json`) contains 3 pieces of
    data (3 items inside the list). Now, we want to set the maximum data
    per database file to 3. If the next data is intended to be added
    to `db_2.json`, it won't be added because the maximum capacity has
    been reached. Instead, a new database file (`db_3.json`) will be
    created to store that new data.
    """
    
    def __init__(self, container:str, /) -> None:
        """
        ### Params
        - `container`: the absolute path to the folder containing the database files

        ### Exceptions
        - `NotADirectoryError`: if `container` is not a directory
        - `AssertionError`: if an item in `container` is not a JSON file
        - Please manually review this function dependencies for more exceptions
        """
        if not _os.path.isdir(container): raise NotADirectoryError(f'Not a dir: {repr(container)}.')
        try:
            if not _same_ext_for_all_dir_files(container, '.json'):
                raise AssertionError(f'All items in {repr(container)} must be JSON files.')
        except (NotADirectoryError, ValueError, AssertionError) as err:
            raise AssertionError(err)
        self.container = container
    
    def _get_blocks(self):
        blocks = _list_dir(self.container)  # Each DB file is called "block"
        blocks = sorted(blocks)  # Sorted from oldest to newest: [oldest, ..., newest]
        return blocks

    @property
    def num_blocks(self) -> int:
        """Number of database files"""
        return len(self._get_blocks())

    def save(self, data:_Any, /, max:int=1024) -> None:
        """
        ### Params:
        - `data`: the new data to be added
        - `max`: maximum data per database file (items inside the list).
                 Will be clamped to at least `0`. `0` and `1` are valid,
                 even though they are truly rarely used.
        """
        blocks = self._get_blocks()

        if blocks == []:  # Handle init case: empty database
            target = _os.path.join(self.container, f'db_{_TimeFmt.sort()}.json')
            db = [data]
            _SafeJSON.write(target, db, do_log=False)
        else:
            target = blocks[-1][1]  # Absolute path to the newest database file
            db = _SafeJSON.read(target)
            if len(db) >= max:
                target = _os.path.join(self.container, f'db_{_TimeFmt.sort()}.json')
                db = [data]
                _SafeJSON.write(target, db, do_log=False)
            else:
                db.append(data)
                _SafeJSON.rewrite(target, db, do_log=False)

    def bulk_save(self, list_of_data:_List[_Any], /, max:int=1024) -> None:
        """Similar to `.save`, but for bulk operations."""
        ## TODO: Implement a much more efficient approach soon
        for data in list_of_data:
            self.save(data, max=max)
            _time.sleep(1/max)  # To prevent collisions in database file names (which happen during testing when `max` is small)

    def get_partial(self, idx:int) -> _List[_Any]:
        """
        Get just a specific database file.

        @param `idx`: `0` for the first file, `1` second, and so on

        ### Exceptions
        - `ValueError`: if `idx` is out of range
        """
        if (idx < 0) or (idx > (self.num_blocks-1)): raise ValueError('Value `idx` out of range.')
        blocks = self._get_blocks()
        pth = blocks[idx][1]
        return _SafeJSON.read(pth)

    def get_all(self) -> _List[_Any]:
        """Get the entire database"""
        out = []
        for _, pth in self._get_blocks():
            out += _SafeJSON.read(pth)
        return out