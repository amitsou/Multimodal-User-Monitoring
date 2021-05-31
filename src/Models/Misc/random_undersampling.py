# -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os


if __name__ == '__main__':
    #Phase 1, balance the dataset and split into train and test
    #Phase 2, split the dataset into train and test and resample the train set

    df = pd.read_csv('actions.csv')
    df.drop(['Date','Time'], axis = 1, inplace = True)
    df = df.loc[(df['Label'] == 0 ) | (df['Label'] == 4)]

    #Show the imbalanced class distribution
    target_count = df.Label.value_counts()
    '''
    print('Class 0:', target_count[0])
    print('Class 4:', target_count[4])
    print('Proportion:', round(target_count[0] / target_count[4], 2), ': 1')
    '''
    target_count.plot(kind='bar', title='Count (target)')
    plt.show()

    #Random Undersampling, removing random records from the majority class
    count_class_0, count_class_4 = df.Label.value_counts()
    df_class_0 = df[df['Label'] == 0]
    df_class_4 = df[df['Label'] == 4]

    df_class_0_under = df_class_0.sample(count_class_4)
    df_random_under = pd.concat([df_class_0_under, df_class_4], axis=0)

    #Show the balanced class distribution
    '''
    print('Random under-sampling:')
    print(df_random_under.Label.value_counts())
    '''
    df_random_under.Label.value_counts().plot(kind='bar', title='Count (target)')
    plt.show()

    #Split into train and test
    X, y = df_random_under.iloc[:,:-1], df_random_under.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    target_names = ['Class0 - Coding','Class4 - Absent']
    names = ['SVM','DT','NB','KNN']
    models = [SVC(), DecisionTreeClassifier(), GaussianNB(), KNeighborsClassifier()]

    scores = []
    for name, clf in zip(names,models):
        clf.fit(X_scaled, y_train)

        score = clf.score(X_test, y_test)
        scores.append(score)
        y_pred = clf.predict(X_test)

        '''
        print(name,'F1 Score:',f1_score(y_test, y_pred, average="macro"))
        print(name,'Precision:',precision_score(y_test, y_pred, average="macro"))
        print(name,'Recall:',recall_score(y_test, y_pred, average="macro"),'\n')
        '''
        print(name,'Classification Report\n',classification_report(y_test, y_pred, target_names = target_names),'\n')

        #Confusion Matrix
        cfm = confusion_matrix(y_true=y_test, y_pred=y_pred)

        #print('Confusion matrix:\n', cfm)
        plt.imshow(cfm, cmap = 'Blues', interpolation='nearest')
        plt.colorbar()
        plt.title('Confusion Matrix for' + ' ' + name)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        tick_marks = np.arange(len(set(y_test))) # length of classes
        class_labels = ['0','4']
        tick_marks
        plt.xticks(tick_marks,class_labels)
        plt.yticks(tick_marks,class_labels)

        # plotting text value inside cells
        thresh = cfm.max() / 2.
        for i,j in itertools.product(range(cfm.shape[0]),range(cfm.shape[1])):
            plt.text(j,i,format(cfm[i,j],'d'),horizontalalignment='center',color='white' if cfm[i,j] >thresh else 'black')
        plt.show()

    #Plotting clfs scores
    df = pd.DataFrame()
    df['Name'] = names
    df['Score'] = scores

    cm = sns.light_palette('green', as_cmap = True)
    s = df.style.background_gradient(cmap = cm)
    sns.set(style = 'whitegrid')
    ax = sns.barplot(y = 'Name', x = 'Score', data = df)
    plt.show()
