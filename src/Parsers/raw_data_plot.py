# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import plot_functions as pt
from Functions import utils as ut

if __name__ == '__main__':
    f1 = '/home/alex/Desktop/Test_Data/Data/Chair/CSV/2021_02_10_02_28_41.csv'
    f2 = '/home/alex/Desktop/Test_Data/Data/Keyboard/CSV/2021_02_10_02_28_41.csv'
    f3 = '/home/alex/Desktop/Test_Data/Data/Mouse/CSV/2021_02_10_02_28_41.csv'
    pt.plot_all_raw(f1,f2,f3)