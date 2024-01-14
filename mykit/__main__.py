

def main():
    print('hello 123 abc')


# if __name__ == '__main__':  # not needed, since the binary `mykit` will execute `main` regardless this line exist or not
#     main()  # not needed, since the binary `mykit` will execute `main` regardless this line exist or not


## devdocs: the `main` doesnt need to be called here since it will be called via (after downloaded from PyPI):
## import sys
## from mykit.__main__ import main
## sys.exit(main())
## Read this for more: https://packaging.python.org/en/latest/specifications/entry-points/#use-for-scripts
