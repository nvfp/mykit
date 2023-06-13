import os
import sys


def add_path():
    """use this function to fix the problem where 'mykit' cannot be accessed"""
    pth = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(pth)