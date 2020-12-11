# -*- coding: utf-8 -*-
import shutil
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))

from Functions import utils as ut

if __name__ == '__main__':
    ut.parse_raw_data('Chair')
    ut.parse_raw_data('Mouse')
    ut.parse_raw_data('Keyboard')