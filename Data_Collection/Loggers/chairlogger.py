# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))

from Functions import utils as ut

if __name__ == '__main__':

    ut.initialize_dirs()
    rec_file = ''.join((ut.get_date(),'.txt'))
    raw_data = ut.get_name('Chair')
    rec_file = os.path.join(raw_data,rec_file)
    ut.record_chair(rec_file)
    print('Exiting logger...')