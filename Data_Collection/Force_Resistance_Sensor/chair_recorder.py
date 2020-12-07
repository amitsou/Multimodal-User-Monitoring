# -*- coding: utf-8 -*-
import chair_functions as cf
import os

if __name__ == '__main__':

    file_extension = '.txt'
    rec_file = 'chair_'+cf.get_date()+file_extension    
    raw_data = cf.create_directories()
    rec_file = os.path.join(raw_data,rec_file)
    cf.get_readings(rec_file)