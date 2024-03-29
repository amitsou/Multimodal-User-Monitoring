# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import utils as ut

if __name__ == '__main__':
    rec_file = ''.join((ut.get_date(),'_',ut.get_time(),'.txt'))
    raw_data = ut.get_name('Chair','Raw')
    rec_file = os.path.join(raw_data,rec_file)
    ut.record_chair(rec_file)
    ut.insert_last_timestamp(rec_file)
    print('Exiting chair logger...')