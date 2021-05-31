# -*- coding: utf-8 -*-
from imblearn.under_sampling import RandomUnderSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
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



def create_tr_tst_dfs(df,class1,class2):
    #Split into train and test
    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, stratify = y)

    target_count = df.Label.value_counts()
    min_n_samples = min(target_count[class1], target_count[class2])

    if target_count[class1] != target_count[class2]:
        os = RandomUnderSampler(sampling_strategy='majority')
        X_new, y_new = os.fit_resample(X_train, y_train)

        print('Original dataset shape {}'.format(Counter(y_train)))
        print('Resampled dataset shape {}'.format(Counter(y_new)))

        #Show the resampled training set class distribution
        resampled_df = X_new
        resampled_df.insert(len(resampled_df.columns),'Label',y_new)
        show_class_distribution(resampled_df,class1,class2,class1_name,class2_name)

        X_new.drop(['Label'], axis = 1, inplace = True)
        return X_new, y_new, X_test, y_test
    else:
        return X_train, y_train, X_test, y_test


def show_class_distribution(X_train,class1,class2,class1_name,class2_name):
    target_count = X_train.Label.value_counts()
    print(class1_name,':', target_count[class1])
    print(class2_name,':', target_count[class2])

    target_count.plot(kind='bar', title='Count (target)')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument('--class1', metavar='class1(int)',help='Please provide class1')
    parser.add_argument('--class2', metavar='class2(int)',help='Please provide class2')

    args = parser.parse_args()
    class1 = int(args.class1)
    class2 = int(args.class2)

    class1_name = ''.join(('Class',str(class1)))
    class2_name = ''.join(('Class',str(class2)))

    df = pd.read_csv('../../actions.csv')
    df.drop(['Date','Time'], axis = 1, inplace = True)
    df = df.loc[(df['Label'] == class1 ) | (df['Label'] == class2)]

    #Show the imbalanced class distribution
    show_class_distribution(df,class1,class2,class1_name,class2_name)


    X_train, y_train, X_test, y_test = create_tr_tst_dfs(df, class1, class2)
    scaler = StandardScaler()
    X_tr_scaled = scaler.fit_transform(X_train)
    X_tst_scaled = scaler.fit_transform(X_test)

    class_labels = [str(class1),str(class2)]
    target_names = [class1_name, class2_name]
    mf.train_test_models(X_tr_scaled,X_tst_scaled,y_train,y_test,target_names,class_labels)
