'''
Created on 26.03.2015

@author: Hsuan-Yu Lin
'''
from distutils.core import setup
from glob import glob
import py2exe

def main():
    data_files = [('Microsoft.VC90.CRT', glob(r'D:\Program Files\Microsoft.VC90.CRT\*.*')), \
                  ('sdl_dll', glob(r'sdl_dll\*.*')), \
                  ('resources', glob(r'resources\*.*')), \
                  ('Data', glob(r'data\*.*'))]
    
    setup(console=['Experiment.py'], data_files = data_files)

if __name__ == '__main__':
    main()
    pass