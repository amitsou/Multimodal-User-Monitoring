# -*- coding: utf-8 -*-
""" usage: python3 feature_extraction.py --segment size 10"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import feature_functions as ft
from Functions import utils as ut

if __name__ == '__main__':

    #Create and save features in .csv files
    segment_size = ut.parse_CLI()
    ft.extract_features(segment_size)

    #Create actions.csv, that contains the whole recordings in it
    #in order to see the class distribution
    #ft.get_all_features() #Reminder: Set the appropriate directory