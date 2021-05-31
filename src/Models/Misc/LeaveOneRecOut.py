# -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#from scipy import interp
from itertools import cycle
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os
import os


path = '/home/alex/Desktop/Test_Data/Data/Features/Segment_size_10'

scaler = StandardScaler()

models = [SVC(), DecisionTreeClassifier(), GaussianNB(), KNeighborsClassifier()]

names = ['SVM','DT','NB','KNN']

target_names = ['Class0-Coding',
                'Class1-Writing Email/Report',
                'Class2-Browsing/Scrolling Social Media',
                'Class3-Browsing/Scrolling Social',
                'Class4-Absent'
]

y_pred_dict = {'SVM':[],'DT':[],'NB':[],'KNN':[]}
y_test_dict = {'SVM':[],'DT':[],'NB':[],'KNN':[]}
results = []

for leaved_one in os.listdir(path):
    train_Set = os.listdir(path).copy()
    train_Set.remove(leaved_one)

    #Training Set -> Concat all test recordings into a dataframe
    list_of_dataframes = []
    for recording in train_Set:
        list_of_dataframes.append(pd.read_csv('/'.join((path,recording))))

    merged_df = pd.concat(list_of_dataframes)
    merged_df.drop(['Date','Time'], axis = 1, inplace = True)
    X_train, y_train = merged_df.iloc[:,:-1], merged_df.iloc[:,-1]

    #Test Set -> leaved recording into another df
    leaved_df = pd.read_csv('/'.join((path,leaved_one)))
    leaved_df.drop(['Date','Time'], axis = 1, inplace = True)
    X_test, y_test = leaved_df.iloc[:,:-1], leaved_df.iloc[:,-1]

    X_tr_scaled = scaler.fit_transform(X_train)
    X_tst_scaled = scaler.fit_transform(X_test)

    scores = []
    for name, clf in zip(names,models):
        clf.fit(X_tr_scaled, y_train)

        score = clf.score(X_tst_scaled, y_test)
        scores.append(score)
        y_pred = clf.predict(X_tst_scaled)

        y_pred_dict[name].append(y_pred.tolist())
        y_test_dict[name].append(y_test.tolist())

    '''
    #Plotting clfs scores
    df = pd.DataFrame()
    df['Name'] = names
    df['Score'] = scores

    cm = sns.light_palette('green', as_cmap = True)
    s = df.style.background_gradient(cmap = cm)
    sns.set(style = 'whitegrid')
    ax = sns.barplot(y = 'Name', x = 'Score', data = df)
    plt.show()
    '''

    del merged_df, leaved_df,scores

#Each clf has a list of lists
#Concatenating each list into a flat list for every key for y_pred_dict
for k,v in y_pred_dict.items():
    tmp=[]
    for i in v:
        if isinstance(i,list):
            tmp.extend(i)
        else:
            tmp.append(i)
    y_pred_dict[k]=tmp

#Each clf has a list of lists
#Concatenating each list into a flat list for every key for y_test_dict
for k,v in y_test_dict.items():
    tmp=[]
    for i in v:
        if isinstance(i,list):
            tmp.extend(i)
        else:
            tmp.append(i)
    y_test_dict[k]=tmp


#Getting predictions and ground_truth for each clf in order to calc. metrics
for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
    print('Y:',k1,v1)
    print('Y_pred:',k2,v2)
    print('Accuracy Score:',accuracy_score(v1,v2))
    print('F1 Score:',f1_score(v1, v2,average='macro'))
    print()
print()