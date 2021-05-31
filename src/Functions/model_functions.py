# -*- coding: utf-8 -*-
from posixpath import curdir
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
from itertools import cycle
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os


def get_train_test_set() -> str:
    dataset_path = '/Data/Features/Segment_size_10'
    current_path = (os.path.abspath(os.curdir))
    os.chdir('../../../')
    current_path = (os.path.abspath(os.curdir))
    current_path1 = ''.join((current_path,dataset_path,'/Train_Set'))
    current_path2 = ''.join((current_path,dataset_path,'/Test_Set'))
    return current_path1,current_path2

def train_test_models(X_tr_scaled,X_tst_scaled,y_train,y_test,target_names,class_labels):
    names = ['SVM','DT','NB','KNN']
    models = [SVC(), DecisionTreeClassifier(), GaussianNB(), KNeighborsClassifier()]
    scores = []
    for name, clf in zip(names,models):
        clf.fit(X_tr_scaled, y_train)

        score = clf.score(X_tst_scaled, y_test)
        scores.append(score)
        y_pred = clf.predict(X_tst_scaled)

        print(name,'Classification Report\n',classification_report(y_test, y_pred, target_names = target_names),'\n')
        plot_confusion_matrix(y_test,y_pred,name,class_labels)

def plot_confusion_matrix(y_test,y_pred,name,class_labels):
    cfm = ""
    cfm = confusion_matrix(y_true=y_test, y_pred=y_pred)

    plt.imshow(cfm, cmap = 'Blues', interpolation='nearest')
    plt.colorbar()
    plt.title('Confusion Matrix for' + ' ' + name)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')

    tick_marks = np.arange(len(set(y_test))) # length of classes
    tick_marks
    plt.xticks(tick_marks,class_labels)
    plt.yticks(tick_marks,class_labels)

    # plotting text value inside cells
    thresh = cfm.max() / 2.
    for i,j in itertools.product(range(cfm.shape[0]),range(cfm.shape[1])):
        plt.text(j,i,format(cfm[i,j],'d'),horizontalalignment='center',color='white' if cfm[i,j] >thresh else 'black')
    plt.show()