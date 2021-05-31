# -*- coding: utf-8 -*-
from sklearn.multiclass import OneVsRestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

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

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys


df = pd.read_csv('actions.csv')
df.drop(['Date','Time'], axis = 1, inplace = True)
df = df.loc[(df['Label'] == 2 ) | (df['Label'] == 3) | (df['Label'] == 4)]

X, y = df.iloc[:,:-1], df.iloc[:,-1]
y = label_binarize(y, classes=[2,3,4])
n_classes = 3

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, stratify=y)
scaler = StandardScaler()
X_tr_scaled = scaler.fit_transform(X_train)
X_tst_scaled = scaler.fit_transform(X_test)

class_names = [2,3,4]
names = ['SVM','DT','NB','KNN']
models = [SVC(), DecisionTreeClassifier(), GaussianNB(), KNeighborsClassifier()]

for name, model in zip(names, models):
    if name == 'SVM':
        clf = OneVsRestClassifier(model)
        y_score = clf.fit(X_tr_scaled, y_train).decision_function(X_tst_scaled)
    else:
        clf = OneVsRestClassifier(model)
        y_score = clf.fit(X_tr_scaled, y_train).predict_proba(X_tst_scaled)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

     # roc for each class
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.plot([0, 1], [0, 1], 'k--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC_AUC for '+name)

    for i in range(n_classes):
        ax.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f) for label %i' % (roc_auc[i], class_names[i]),linewidth=2.5)

    ax.legend(loc="best")
    ax.grid(alpha=.4)
    sns.despine()
    plt.show()