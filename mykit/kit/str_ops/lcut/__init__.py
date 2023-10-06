

## Birthdate: Oct 6, 2023
def lcut(input_str:str, unwanted:str, check:bool=False) -> str:
    """
    left-cut (lcut). Trim the beginning characters `unwanted` from the given `input_str`.

    ## Params
    - `input_str`: the input string
    - `unwanted`: the characters to be trimmed from the beginning (see examples below to learn more)
    - `check`: if `True`, raise an exception (see below) if `input_str` does not start with `unwanted`

    ## Exceptions
    - `ValueError` if `unwanted` is an empty string
    - `AssertionError` if `input_str` doesn't start with `unwanted` when `check` is `True`

    ## Examples
    - `lcut('121foo', '12')` -> `'1foo'`
    - `lcut('123 hi mom 123', '123 ')` -> `'hi mom 123'`
    - `lcut('hi mom', 'cool')` -> `'hi mom'`

    ## Docs
    - the reason using `lcut` and not `lstrip` is because `'123123 hi mom 123'.lstrip('123')` will be `' hi mom 123'`
    """

    ## Check
    if unwanted == '': raise ValueError("lcut: `unwanted` shouldn't be an empty string.")

    if input_str.startswith(unwanted):
        return input_str[len(unwanted):]
    else:
        if check:
            raise AssertionError("lcut: the given `input_str` does not start with `unwanted`.")
        return input_str
