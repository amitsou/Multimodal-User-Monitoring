# -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn import metrics
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



def check_empty_file(df1, df2):
    #Checks for an empty dataframe
    #Return:True or False
    return True if(df1.empty or df2.empty ) else False


'''
def get_all_features(train_set):
    #Concatenate pandas dataframes
    #Return: x's and y's respectively

    #abs_path = os.getcwd() + '/Features'
    abs_path = '/home/alex/Desktop/Test_Data/Data/Features/Segment_size_10'
    list_of_dataframes = []

    if type(train_set) == str: #for leaved_one
        leaved_df = pd.read_csv(abs_path + '/' + train_set)
        #leaved_df.fillna(int(0), inplace=True)
        del leaved_df['Time'], leaved_df['Date']
        return leaved_df.iloc[:,:-1], leaved_df.iloc[:,-1]
    else:
        for filename in train_set:
            list_of_dataframes.append(pd.read_csv(abs_path + '/' + filename))
        merged_df = pd.concat(list_of_dataframes)
        #merged_df.fillna(int(0), inplace=True)
        del merged_df['Time'], merged_df['Date']
        return merged_df.iloc[:,:-1], merged_df.iloc[:,-1]
'''


def binary_classification(train_set):
    '''Concatenate pandas dataframes
       Return: x's and y's respectively
    '''
    #abs_path = os.getcwd() + '/Features'
    abs_path = '/home/alex/Desktop/Test_Data/Data/Features/Segment_size_10'
    list_of_dataframes = []

    if type(train_set) == str: #for leaved_one
        leaved_df = pd.read_csv(abs_path + '/' + train_set)

        leaved_df.drop(['Date','Time'],axis = 1, inplace = True)
        leaved_df = leaved_df.loc[(leaved_df['Label'] == 0 ) | (leaved_df['Label'] == 4)]
        leaved_df['Label'] = leaved_df['Label'].replace(4,1)

        return leaved_df.iloc[:,:-1], leaved_df.iloc[:,-1]
    else:
        for filename in train_set:
            list_of_dataframes.append(pd.read_csv(abs_path + '/' + filename))

        merged_df = pd.concat(list_of_dataframes)
        merged_df.drop(['Date','Time'],axis = 1, inplace = True)
        merged_df = merged_df.loc[(merged_df['Label'] == 0 ) | (merged_df['Label'] == 4)]
        merged_df['Label'] = merged_df['Label'].replace(4,1)

        return merged_df.iloc[:,:-1], merged_df.iloc[:,-1]


if __name__ == '__main__':
    '''
    df = pd.read_csv(os.getcwd() + '/actions_new.csv')
    df.hist(figsize = (25,30))
    plt.savefig("Bar Plot2.pdf")
    plt.show()

    unique, counts = np.unique(df['Label'], return_counts=True)
    plt.bar(unique, counts)
    plt.title('Class Frequency')
    plt.xlabel('Class')
    plt.ylabel('Frequency')
    plt.show()
    sys.exit()
    '''

    path = '/home/alex/Desktop/Test_Data/Data/Features/Segment_size_10'
    features = os.listdir(path)

    models = [('LDA', LinearDiscriminantAnalysis()),
              ('kNN', KNeighborsClassifier()),
              ('DT',  DecisionTreeClassifier()),
              ('NB',  GaussianNB()),
              ('SVM', SVC())
    ]


    #Build binary classifiers
    y_pred_dict = {'LDA':[],'kNN':[],'DT':[],'NB':[],'SVM':[]}
    y_test_dict = {'LDA':[],'kNN':[],'DT':[],'NB':[],'SVM':[]}
    results = []
    scaler = StandardScaler()
    for leaved_one in features:
        train_Set = features.copy()
        train_Set.remove(leaved_one)


        print("Leaved", leaved_one)
        print("Train", train_Set)
        print("+++++++++++++++++++++++++++++++++++++++++++++")


        training_x, training_y = binary_classification(train_Set) #reading train data
        test_x, test_y = binary_classification(leaved_one)#reading test data

        if(check_empty_file(training_x,training_y) or check_empty_file(test_x,test_y)):#to kanoyme giati theloume mono 2 klaseis
            #print('Found empty df')
            continue

        training_x, training_y = training_x.to_numpy(), training_y.to_numpy()
        test_x, test_y = test_x.to_numpy(), test_y.to_numpy()
        scaled_x = scaler.fit_transform(training_x)

        for name, model in models:
            model.fit(scaled_x, training_y)
            predicted = model.predict(test_x)

            y_pred_dict[name].append(predicted.tolist())
            y_test_dict[name].append(test_y.tolist())


    for k,v in y_pred_dict.items(): #concat the list of lists (dict values) into a flat list for every key
        tmp=[]
        for i in v:
            if isinstance(i,list):
                tmp.extend(i)
            else:
                tmp.append(i)
        y_pred_dict[k]=tmp

    for k,v in y_test_dict.items(): #concat the list of lists (dict values) into a flat list for every key
        tmp=[]
        for i in v:
            if isinstance(i,list):
                tmp.extend(i)
            else:
                tmp.append(i)
        y_test_dict[k]=tmp

    #Metrics
    for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
        #print('Y:',k1,v1)
        #print('Y_pred:',k2,v2)

        print('Accuracy Score:',accuracy_score(v1,v2))
        print('F1 Score:',f1_score(v1, v2,average='binary'))
        print()
    print()
    sys.exit()

    array = np.zeros(shape=(2,2))
    for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
            array =+ confusion_matrix(v1, v2)

    df_cm = pd.DataFrame(array, range(2), range(2))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    plt.show()


    '''
    y_pred_dict = {'LDA':[],'kNN':[],'DT':[],'NB':[],'SVM':[]}
    y_test_dict = {'LDA':[],'kNN':[],'DT':[],'NB':[],'SVM':[]}
    results = []
    scaler = StandardScaler()

    for leaved_one in features:
        train_Set = features.copy()
        train_Set.remove(leaved_one)

        #print("Leaved", leaved_one)
        #print("Train", train_Set)
        #print("+++++++++++++++++++++++++++++++++++++++++++++")

        training_x, training_y = get_all_features(train_Set) #reading train data
        test_x, test_y = get_all_features(leaved_one)#reading test data
        scaled_x = scaler.fit_transform(training_x)

        for name, model in models:
            model.fit(scaled_x, training_y)
            predicted = model.predict(test_x)
            y_pred_dict[name].append(predicted.tolist())
            y_test_dict[name].append(test_y.tolist())


    for k,v in y_pred_dict.items(): #concat the list of lists (dict values) into a flat list for every key
        tmp=[]
        for i in v:
            if isinstance(i,list):
                tmp.extend(i)
            else:
                tmp.append(i)
        y_pred_dict[k]=tmp

    for k,v in y_test_dict.items(): #concat the list of lists (dict values) into a flat list for every key
        tmp=[]
        for i in v:
            if isinstance(i,list):
                tmp.extend(i)
            else:
                tmp.append(i)
        y_test_dict[k]=tmp

    #Metrics
    for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
        print(k1)
        print('Accuracy Score:',accuracy_score(v1,v2))
        print('F1 Score:',f1_score(v1, v2, average='macro'))
        print()
    print()

    #for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
    #        array = confusion_matrix(v1, v2)
    #        df_cm = pd.DataFrame(array, range(5), range(5))
    #        sn.set(font_scale=1.4) # for label size
    #        sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    #        plt.title(k1, fontsize = 20)
    #        plt.show()

    #add every array
    array = np.zeros(shape=(5,5))
    for (k1,v1), (k2,v2) in zip(y_test_dict.items(), y_pred_dict.items()):
            array =+ confusion_matrix(v1, v2)
            #print(array)
    print(array)
    df_cm = pd.DataFrame(array, range(5), range(5))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size
    plt.show()
    '''