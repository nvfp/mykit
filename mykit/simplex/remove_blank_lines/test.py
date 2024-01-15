from . import remove_blank_lines

import os

DIR = os.path.join(os.path.dirname(__file__), 'test_data')

def go():
    f1 = os.path.join(DIR, 'k1_before.py')
    f2 = os.path.join(DIR, 'k1_after.py')
    remove_blank_lines(f1)
    with open(f1, 'r') as f: t1 = f.read()
    with open(f2, 'r') as f: t2 = f.read()
    #tt.eq(t1, t2, "both file are the same")

def empty_file_is_no_change():  # No changes if an empty file
    f1 = os.path.join(DIR, 'k2_before.py')
    f2 = os.path.join(DIR, 'k2_after.py')
    remove_blank_lines(f1)
    with open(f1, 'r') as f: t1 = f.read()
    with open(f2, 'r') as f: t2 = f.read()
    #tt.eq(t1, t2, "empty files")

def complex_file():
    f1 = os.path.join(DIR, 'k3_before.py')
    f2 = os.path.join(DIR, 'k3_after.py')
    remove_blank_lines(f1)
    with open(f1, 'r') as f: t1 = f.read()
    with open(f2, 'r') as f: t2 = f.read()
    #tt.eq(t1, t2, "complex one")
