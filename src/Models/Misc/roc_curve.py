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

'''
def show_cm(y_true, y_pred, class_names=None, model_name=None):
    #Show confusion matrix
    cf = confusion_matrix(y_true, y_pred)
    plt.imshow(cf, cmap=plt.cm.Blues)
    if model_name:
        plt.title(“Confusion Matrix: {}”.format(model_name))
    else:
        plt.title(“Confusion Matrix”)
        plt.ylabel(“True Label”)
        plt.xlabel(“Predicted Label”)
    if class_names:
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names)
        plt.yticks(tick_marks, class_names)
    else:
        class_names = set(y_true)
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names)
        plt.yticks(tick_marks, class_names)
        thresh = cf.max() / 2.0
    for i, j in itertools.product(range(cf.shape[0]),
                            range(cf.shape[1])):
        plt.text(j, i, cf[i, j],
                 horizontalalignment=”center”,
                 color=”white” if cf[i, j] > thresh else “black”,
        )
    plt.colorbar()


def get_auc_scores(clf, X_train, X_test, y_train, y_test):
   #Prints the AUC scores for training and testing data
   #and returns testing score
    y_train_score = clf.predict_proba(X_train)[:, 1]
    y_test_score = clf.predict_proba(X_test)[:, 1]
    auc_train = roc_auc_score(y_train, y_train_score)
    auc_test = roc_auc_score(y_test, y_test_score)
    #print('Training AUC':{auc_train},Testing AUC: {auc_test}”””)
    return y_test_score


def plot_roc_curve(y_test, y_test_score):
    #Plot ROC curve for testing data
    fpr, tpr, _ = roc_curve(y_test, y_test_score)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label=”ROC curve (area = %0.2f)” % roc_auc)
    plt.plot([0, 1], [0, 1], “k — “)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel(“False Positive Rate”)
    plt.ylabel(“True Positive Rate”)
    plt.title(“Receiver operating characteristic”)
    plt.legend(loc=”lower right”)
    plt.show()
'''


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

#names = ['SVM','DT','NB','KNN']
clf = OneVsRestClassifier(SVC())
y_score = clf.fit(X_tr_scaled, y_train).decision_function(X_tst_scaled)

'''
    #clf = OneVsRestClassifier(KNeighborsClassifier())
    #clf = OneVsRestClassifier(GaussianNB())
    #clf = OneVsRestClassifier(DecisionTreeClassifier())
    #y_score = clf.fit(X_tr_scaled, y_train).predict_proba(X_tst_scaled)
'''

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
ax.set_title('ROC')
for i in range(n_classes):
    ax.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f) for label %i' % (roc_auc[i], i),linewidth=2.5)
ax.legend(loc="best")
ax.grid(alpha=.4)
sns.despine()
plt.show()


'''
# Plot of a ROC curve for a specific class
for i in range(n_classes):
    plt.figure()
    plt.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f)' % roc_auc[i])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()
'''