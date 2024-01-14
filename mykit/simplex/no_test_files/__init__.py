import os


def no_test_files(dir_pth:str, /, tell:bool=True, speaker=None) -> None:
    """
    A standalone function for build system: delete all files with the name "test.py".
    
    ## Params
    - `dir_pth`: the abspath to the folder (will delete all "test.py" recursively inside this dir).
                    make sure only files and folders are inside.
    - `tell`: do logging to inform the deleted file.
    - `speaker`: the logging handler. if None, will use `print`.
    """

    for i in sorted(os.listdir(dir_pth)):
        ipth = os.path.join(dir_pth, i)

        if os.path.isfile(ipth):
            if i.lower() == 'test.py':
                if tell:
                    if speaker is None:
                        print(f"INFO: Removing file: {repr(ipth)}")
                    else:
                        speaker(f"Removing file: {repr(ipth)}")
                os.remove(ipth)
        
        # elif os.path.isdir(ipth): no_test_files(ipth, tell, speaker)
        # else: raise AssertionError(f"Unknown: {repr(ipth)}")
        ## vvvvvvvv assuming there are just files and dirs
        else: no_test_files(ipth, tell, speaker)
