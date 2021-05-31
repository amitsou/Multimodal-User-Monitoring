# -*- coding: utf-8 -*-
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from collections import Counter
from itertools import cycle
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../../../"))
from Functions import model_functions as mf


def get_train_test_set() -> str:
    current_path = (os.path.abspath(os.curdir))
    os.chdir('../../..')

    dataset_path = '/Data/Features/Segment_size_10'
    current_path = (os.path.abspath(os.curdir))

    current_path1 = ''.join((current_path,dataset_path,'/Train_Set'))
    current_path2 = ''.join((current_path,dataset_path,'/Test_Set'))
    return current_path1,current_path2

def create_tr_tst_dfs(tr_set,tr_path,tst_set,tst_path,class1,class2,class3,class1_name,class2_name,class3_name):
    list_of_dataframes = []
    for f in tst_set:
        list_of_dataframes.append(pd.read_csv('/'.join((tst_path,f))))

    tst_df = pd.concat(list_of_dataframes)
    tst_df.drop(['Date','Time'], axis = 1, inplace = True)
    tst_df = tst_df.loc[(tst_df['Label'] == class1 ) | (tst_df['Label'] == class2) | (tst_df['Label'] == class3)]
    X_test, y_test = tst_df.iloc[:,:-1], tst_df.iloc[:,-1]

    list_of_dataframes = []
    for f in tr_set:
        list_of_dataframes.append(pd.read_csv('/'.join((tr_path,f))))

    tr_df = pd.concat(list_of_dataframes)
    tr_df.drop(['Date','Time'], axis = 1, inplace = True)
    tr_df = tr_df.loc[(tr_df['Label'] == class1 ) | (tr_df['Label'] == class2) | (tr_df['Label'] == class3)]

    #Show the training set class distribution
    show_class_distribution(tr_df,class1,class2,class3,class1_name,class2_name,class3_name)

    X_train, y_train = tr_df.iloc[:,:-1], tr_df.iloc[:,-1]
    target_count = tr_df.Label.value_counts()
    min_n_samples = min(target_count[class1], target_count[class2], target_count[class3])

    if target_count[class1] != target_count[class2] != target_count[class3]:
        os = RandomUnderSampler(sampling_strategy={class1:min_n_samples, class2:min_n_samples, class3:min_n_samples})
        X_new, y_new = os.fit_resample(X_train, y_train)

        print('Original dataset shape {}'.format(Counter(y_train)))
        print('Resampled dataset shape {}'.format(Counter(y_new)))

        #Show the resampled training set class distribution
        resampled_df = X_new
        resampled_df.insert(len(resampled_df.columns),'Label',y_new)
        show_class_distribution(resampled_df,class1,class2,class3,class1_name,class2_name,class3_name)

        X_new.drop(['Label'], axis=1, inplace=True)
        return X_new, y_new, X_test, y_test
    else:
        return X_train,y_train,X_test,y_test

def show_class_distribution(X_train,class1,class2,class3,class1_name,class2_name,class3_name):
    target_count = X_train.Label.value_counts()
    print(class1_name,':', target_count[class1])
    print(class2_name,':', target_count[class2])
    print(class3_name,':', target_count[class3])
    target_count.plot(kind='bar', title='Count (target)')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument('--class1',metavar='class1(int)',help='Please provide class1')
    parser.add_argument('--class2',metavar='class2(int)',help='Please provide class2')
    parser.add_argument('--class3',metavar='class3(int)',help='Please provide class3')

    args = parser.parse_args()
    class1 = int(args.class1)
    class2 = int(args.class2)
    class3 = int(args.class3)

    class1_name = ''.join(('Class',str(class1)))
    class2_name = ''.join(('Class',str(class2)))
    class3_name = ''.join(('Class',str(class3)))

    tr_path, tst_path = get_train_test_set()
    tr_set = os.listdir(tr_path)
    tst_set = os.listdir(tst_path)

    X_train, y_train, X_test, y_test = create_tr_tst_dfs(tr_set,tr_path,tst_set,tst_path,class1,class2,class3,class1_name,class2_name,class3_name)
    scaler = StandardScaler()
    X_tr_scaled = scaler.fit_transform(X_train)
    X_tst_scaled = scaler.fit_transform(X_test)

    class_labels = [str(class1),str(class2),str(class3)]
    target_names = [class1_name, class2_name, class3_name]

    mf.train_test_models(X_tr_scaled,X_tst_scaled,y_train,y_test,target_names,class_labels)