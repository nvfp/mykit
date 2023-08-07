import os as _os
import uuid as _uuid


## Ref: https://github.com/orgs/community/discussions/28146

def set_output(name, value):
    """
    ## Demo
    >>> set_output('foo', '123')
    """
    with open(_os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

def set_multiline_output(name, value):
    with open(_os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = _uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)