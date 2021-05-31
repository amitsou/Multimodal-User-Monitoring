# -*- coding: utf-8 -*-
from xgboost import XGBClassifier

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import LeaveOneOut

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler

import matplotlib.pyplot as plt
import imblearn
import pandas as pd
import numpy as np
import seaborn as sn
import sys
import os


'''
def show_confusion_matrix(y_test,y_pred):
    conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
    print('Confusion matrix:\n', conf_mat)

    labels = ['Class 0', 'Class 4']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(conf_mat, cmap=plt.cm.Blues)
    fig.colorbar(cax)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    plt.xlabel('Predicted')
    plt.ylabel('Expected')
    plt.show()
'''


def plot_2d_space(X, y, label='Classes'):
    colors = ['#1F77B4', '#FF7F0E']
    markers = ['o', 's']

    for l, c, m in zip(np.unique(y), colors, markers):
        plt.scatter(X[y==l, 0],
                    X[y==l, 1],
                    c=c, label=l, marker=m
        )
    plt.title(label)
    plt.legend(loc='upper right')
    plt.show()




if __name__ == '__main__':

    df = pd.read_csv('actions.csv')
    df.drop(['Date','Time'], axis = 1, inplace = True)
    df = df.loc[(df['Label'] == 0 ) | (df['Label'] == 4)]

    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    pca = PCA(n_components=2)
    X = pca.fit_transform(X)
    plot_2d_space(X, y, 'Imbalanced dataset')


    #Show the imbalanced class distribution
    target_count = df.Label.value_counts()
    print('Class 0:', target_count[0])
    print('Class 4:', target_count[4])
    print('Proportion:', round(target_count[0] / target_count[4], 2), ': 1')
    target_count.plot(kind='bar', title='Count (target)')
    plt.show()

    '''IMBLEARN '''
    #create a 2-dimensional plot function, plot_2d_space, to see the data distribution:
    #Because the dataset has many dimensions (features) and our graphs will be 2D,
    #we will reduce the size of the dataset using Principal Component Analysis (PCA):
    #X, y = df.iloc[:,:-1], df.iloc[:,-1]
    #pca = PCA(n_components=2)
    #X = pca.fit_transform(X)
    #plot_2d_space(X, y, 'Imbalanced dataset (2 PCA components)')


    #Random under-sampling and over-sampling with imbalanced-learn
    rus = RandomUnderSampler(sampling_strategy='majority')
    X_rus, y_rus = rus.fit_resample(X, y)
    colors = ['white' if v == 0 else 'black' if v == 4 else '#67a9cf' for v in y_rus]
    sys.exit()

    #df_test_under.Label.value_counts().plot(kind='bar', title='Count (target)')
    plot_2d_space(X_rus, y_rus, 'Random under-sampling')

    ros = RandomOverSampler(sampling_strategy='minority')
    X_ros, y_ros = ros.fit_resample(X, y)
    print(X_ros.shape[0] - X.shape[0], 'new random picked points')
    plot_2d_space(X_ros, y_ros, 'Random over-sampling')

    ''' Random Sampling df.Sample '''
    #Let's implement a basic example, which uses the DataFrame.sample method to get random samples each class
    #Random Undersampling, removing random records from the majority class
    count_class_0, count_class_4 = df.Label.value_counts()
    df_class_0 = df[df['Label'] == 0]
    df_class_4 = df[df['Label'] == 4]

    df_class_0_under = df_class_0.sample(count_class_4)
    df_test_under = pd.concat([df_class_0_under, df_class_4], axis=0)

    #Show the balanced class distribution
    print('Random under-sampling:')
    print(df_test_under.Label.value_counts())
    df_test_under.Label.value_counts().plot(kind='bar', title='Count (target)')
    plt.show()


    #Random Over-Sampling, duplicate random records from the minority class
    df_class_1_over = df_class_4.sample(count_class_0, replace=True)
    df_test_over = pd.concat([df_class_0, df_class_1_over], axis=0)

    #Show the balanced class distribution
    print('Random over-sampling:')
    print(df_test_over.Label.value_counts())
    df_test_over.Label.value_counts().plot(kind='bar', title='Count (target)')
    plt.show()

    '''
    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X_train)
    '''

    '''
    #XGBOOST classifier
    model = XGBClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    show_confusion_matrix(y_test,y_test)

    #XGBOOST classifier with one feature to reduce accuracy
    model = XGBClassifier()
    model.fit(X_train[['Velocity_X']], y_train)
    y_pred = model.predict(X_test[['Velocity_X']])
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    #Confusion Matrix
    show_confusion_matrix(y_test,y_test)
    '''




    '''
    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    y = y.to_numpy()



    models = [('SVM', SVC()),
              ('DT', DecisionTreeClassifier()),
              ('NB', GaussianNB()),
              ('KNN', KNeighborsClassifier())
    ]
    '''
