# -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sn
import sys
import os


if __name__ == '__main__':

    df = pd.read_csv('actions_new.csv')
    df.drop(['Date','Time'], axis = 1, inplace = True)
    df = df.loc[(df['Label'] == 0 ) | (df['Label'] == 4)]

    unique, counts = np.unique(df['Label'], return_counts=True)
    plt.bar(unique, counts)
    plt.title('Class Frequency')
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.show()

    df['Label'] = df['Label'].replace(4,0) #For binary classification

    X, y = df.iloc[:,:-1], df.iloc[:,-1]
    y = y.to_numpy()

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)

    models = [('SVM', SVC()),
              ('DT', DecisionTreeClassifier()),
              ('NB', GaussianNB()),
              ('KNN', KNeighborsClassifier())
    ]

    for name,model in models:
        y_pred = cross_val_score(model, scaled_X, y, scoring='accuracy', cv=LeaveOneOut(), n_jobs=-1)

        print(name,'','F1 Score:',f1_score(y,y_pred,average='binary'),'','Accuracy: %.3f (%.3f)' % (np.mean(y_pred),np.std(y_pred)),'\n')

        df_cm = pd.DataFrame(confusion_matrix(y,y_pred), range(2), range(2))
        sn.set(font_scale=1.4) # for label size
        sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
        plt.show()