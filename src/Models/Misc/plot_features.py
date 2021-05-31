# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sn
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import plot_functions as pt
from Functions import utils as ut



if __name__ == '__main__':

    pd.options.mode.chained_assignment = None
    np.set_printoptions(suppress=True)
    df = pd.read_csv('actions.csv')
    df.drop(['Date','Time'], axis = 1, inplace = True)

    #Extract features for every class
    class0 = df.loc[(df['Label'] == 0 )]
    class0.drop('Label', axis = 1, inplace = True)
    class0 = class0.to_numpy()

    class1 = df.loc[(df['Label'] == 1 )]
    class1.drop('Label', axis = 1, inplace = True)
    class1 = class1.to_numpy()

    class2 = df.loc[(df['Label'] == 2 )]
    class2.drop('Label', axis = 1, inplace = True)
    class2 = class2.to_numpy()

    class3 = df.loc[(df['Label'] == 3 )]
    class3.drop('Label', axis = 1, inplace = True)
    class3 = class3.to_numpy()

    class4 = df.loc[(df['Label'] == 4 )]
    class4.drop('Label', axis = 1, inplace = True)
    class4 = class4.to_numpy()
    del df

    print(class0.shape)
    print(class1.shape)
    print(class2.shape)
    print(class3.shape)
    print(class4.shape)
    sys.exit()

    feature_names = ['Velocity_X',
                     'Velocity_Y',
                     'Clicks',
                     'R_Clicks',
                     'L_Clicks',
                     'M_Clicks',
                     'All_keys_N',
                     'Arrow_keys_N',
                     'Spaces_N',
                     'Shft_Ctrl_Alt_N',
                     'M_A0',
                     'STD_A0',
                     'M_A1',
                     'STD_A1',
                     'M_A2',
                     'STD_A',
                     'M_A3',
                     'STD_A3',
                     'M_A4',
                     'STD_A4'
    ]


    class_names = ['Class0',
                   'Class1',
                   'Class2',
                   'Class3',
                   'Class4'
    ]


    feature_mtr = [class0,class1,class2,class3,class4]
    pt.plot_feature_histograms(feature_mtr,feature_names,class_names)