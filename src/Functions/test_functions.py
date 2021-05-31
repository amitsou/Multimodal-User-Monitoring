# -*- coding: utf-8 -*-
from serial import Serial
from datetime import datetime, timedelta
import pandas as pd
import collections
import argparse
import logging
import shutil
import serial
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import plot_functions as pt
from Functions import utils as ut


def get_dirs_by_date(modality):
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))
    os.chdir('./Data')
    current_path = (os.path.abspath(os.curdir))
    current_path = os.path.join(current_path,ut.get_date(),modality)
    raw_data_path = os.path.join(current_path,'Raw')
    csv_data_path = os.path.join(current_path,'CSV')
    edited_logs_path = os.path.join(current_path,'Edited_logs')
    features_path = os.path.join(current_path,'Features')

    return raw_data_path, csv_data_path, edited_logs_path, features_path

def initialize_dirs_by_date():
    """Create the appropriate directories in order to save
       and process the collected data
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir)) #Parent folder
    current_path = os.path.join(current_path,'Data')
    ut.create_subdirs([current_path])

    #Create the date folder
    current_path = os.path.join(current_path,ut.get_date())
    ut.create_subdirs([current_path])

    #Create the feature folder
    features = os.path.join(current_path,'Features')
    ut.create_subdirs([features])

    #Create mouse log folder
    mouse = os.path.join(current_path,'Mouse')
    ut.create_subdirs([mouse])
    #Create mouse subfolders
    names = ut.concat_names(mouse)
    ut.create_subdirs(names)

    #Create keyboard log  folder
    keyboard = os.path.join(current_path,'Keyboard')
    ut.create_subdirs([keyboard])
    #Create keyboard subfolders
    names = ut.concat_names(keyboard)
    ut.create_subdirs(names)

    #Create the chair log folder
    chair = os.path.join(current_path,'Chair')
    ut.create_subdirs([chair])
    #Create chair subfolders
    names = ut.concat_names(chair)
    ut.create_subdirs(names)

    #Create webcam log folder
    webcam = os.path.join(current_path,'Webcam')
    ut.create_subdirs([webcam])

def get_name_by_date(modality,dest) -> str:
    """Save the recorded log into /Data/Date/<Modality_name>/Raw

    Args:
        modality (str): The log data source
        dest(str): The folder to save the data
    Returns:
        str: The absolute path where each recording is saved
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))
    current_path = os.path.join(current_path,'Data',ut.get_date())

    if modality == 'Chair':
        chair_path = os.path.join(current_path,modality,dest)
        return chair_path

    elif modality == 'Mouse':
        mouse_path = os.path.join(current_path,modality,dest)
        return mouse_path

    elif modality == 'Keyboard':
        keyboard_path = os.path.join(current_path,modality,dest)
        return keyboard_path

def parse_raw_data_by_date(modality):
    """Convert each modality's raw data into csv format and move
       the edited raw data into the appropriate Edited_logs folder

    Args:
        modality (str): The data source
    """
    raw_data_path, csv_data_path, edited_logs_path,_ = get_dirs_by_date(modality)

    txt_names = ut.crawl_dir('.txt',raw_data_path)
    csv_names = []
    for elem in txt_names:
        name = elem.split('/')[-1].split('.')[0]
        csv_name = name+'.csv'
        tmp = os.path.join(csv_data_path,csv_name)
        csv_names.append(tmp)

    if modality == 'Mouse':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
            #for i in range(len(txt_names)):
                ut.convert_mouse2_csv(txt_names[i],csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)

    elif modality == 'Keyboard':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
            #for i in range(len(txt_names)):
                ut.convert_keys2_csv(txt_names[i],csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)

    elif modality == 'Chair':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
            #for i in range(len(txt_names)):
                ut.convert_chair_2_csv(txt_names[i],csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)


'''
#todo examine this function
def concat_and_save_features(f1,s1,f2,s2,f3,s3,chair):
    """Concatenate the given features on timestampt

    Args:
        f1 (np.array): Mouse Features
        s1 (np.array): Mouse Seconds
        f2 (np.array): Keyboard Features
        s2 (np.array): Keyboard Seconds
        f3 (np.array): Chair Features
        s3 (np.array): Chair Seconds
        chair: Chair Raw .csv file
    """
    chair_df = pd.read_csv(chair)
    chair_df['Time'] = chair_df['Time'].str.split(',').str[0]

    df1 = pd.DataFrame(f1, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
    df1['Time'] = convert_seconds(s1)

    df2 = pd.DataFrame(f2, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
    df2['Time'] = convert_seconds(s2)

    df3 = pd.DataFrame(f3, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
    df3['Time'] = convert_seconds(s3)

    data_frames = [df1, df2, df3]
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Time'],how='outer'), data_frames).fillna('0.0')
    df_merged.sort_values(by='Time', inplace=True, ascending=True)
    col = df_merged.pop('Time')
    df_merged.insert(0, col.name, col)
    del df1, df2, df3

    df = pd.merge( chair_df, df_merged, on=['Time'])
    df.drop(['Date','A0','A1','A2','A3','A4'], axis = 1, inplace = True)

    column_names = ['Time',
                    'Velocity_X',
                    'Velocity_Y',
                    'Clicks',
                    'R_Clicks',
                    'L_Clicks',
                    'M_Clicks',
                    'All_keys_N',
                    'Arrow_keys_N',
                    'Spaces_N',
                    'Shft_Ctrl_Alt_N',
                    'M_A0',
                    'STD_A0',
                    'M_A1',
                    'STD_A1',
                    'M_A2',
                    'STD_A2',
                    'M_A3',
                    'STD_A3',
                    'M_A4',
                    'STD_A4',
                    'Label'
    ]

    df = df.reindex(columns=column_names)
    features_file = ''.join((chair.split('/')[-1].split('.')[0],'.csv'))
    features_dir = get_features()
    features_file = os.path.join(features_dir,features_file)
    df.to_csv(features_file, encoding='utf-8', index=False)
'''

'''
def cmp_segments_tuple(mouse,keyboard,chair,segment_size) -> bool:
    """Given a tuple of recordings for three modalities, examine whether a
       file contains a smaller second number than the segment size

    Args:
        mouse (str): Mouse .csv abs path
        keyboard (str): Keyboard .csv abs path
        chair (str): Chair .csv abs path
        segment_size (int): The given segment size

    Returns:
        bool: True or False
    """
    files = [mouse, keyboard, chair]
    sec_dif = []
    for filename in files:
        temp_df = pd.read_csv(filename)
        temp_df['Time'] = temp_df['Time'].str.split(',').str[0]

        last = temp_df.loc[temp_df.index[-1], 'Time']
        last = pd.to_datetime(last)
        first = temp_df.loc[temp_df.index[0], 'Time']
        first = pd.to_datetime(first)

        sec_dif.append((last - first).seconds)
        del temp_df
    return False if (sec_dif[0] < segment_size or sec_dif[1] < segment_size or sec_dif[2] < segment_size) else True
'''


'''
def extract_features(segment_size):
    """Extract and save features based on session recordings

    Args:
        segment_size (int): Segment size(Chunk size) in seconds
    """
    mouse,keyboard,chair = get_recordings()
    pairs = [(i, j, k) for i in mouse for j in keyboard for k in chair if i.split('/')[-1].split('.')[0] == j.split('/')[-1].split('.')[0] == k.split('/')[-1].split('.')[0]]

    column_names = ['Time',
                    'Velocity_X',
                    'Velocity_Y',
                    'Clicks',
                    'R_Clicks',
                    'L_Clicks',
                    'M_Clicks',
                    'All_keys_N',
                    'Arrow_keys_N',
                    'Spaces_N',
                    'Shft_Ctrl_Alt_N',
                    'M_A0',
                    'STD_A0',
                    'M_A1',
                    'STD_A1',
                    'M_A2',
                    'STD_A2',
                    'M_A3',
                    'STD_A3',
                    'M_A4',
                    'STD_A4',
                    'Label'
    ]

    for m,k,c in pairs:
        print(m)
        print(k)
        print(c,'\n')

        #Examine segments and the recorded seconds number for each file
        m_res = cmp_segments(m, segment_size)
        k_res = cmp_segments(k, segment_size)

        if(m_res):
            print('Mouse is missing')
            continue
            kf, kt, k_start = get_key_features(k,float(segment_size))
            cf, ct, c_start = get_chair_features(c,float(segment_size))

            print(kf)
            print(kt)
            res1 = convert_seconds(kt)
            print(res1)
            print(len(kf), len(kt))
            print(k_start)

            print(cf)
            print(ct)
            res2 = convert_seconds(ct)
            print(res2)
            print(len(cf), len(ct))
            print(c_start)

            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
            tmp = compare(res1, res2)
            if(tmp == False):
                for i,j in zip(res1, res2):
                    if(i == j):
                        print('i:',i,'j:',j)
                    else:
                        print('i:',i,'j:',j)

            print('Are the lists identical? :',tmp)
            #sys.exit()
            continue

            chair_df = pd.read_csv(c)
            chair_df['Time'] = chair_df['Time'].str.split(',').str[0]
            df1 = pd.DataFrame(kf, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
            df1['Time'] = convert_seconds(kt)
            df2 = pd.DataFrame(cf, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
            df2['Time'] = convert_seconds(ct)

            #REVIEW STO AGGREGATION
            data_frames = [df1, df2]
            df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Time'],how='outer'), data_frames).fillna('0.0')
            df_merged.sort_values(by='Time', inplace=True, ascending=True)

            #Add Columns
            df_merged.insert(loc=0, column='Velocity_X', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=1, column='Velocity_Y', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=2, column='Clicks', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=3, column='R_Clicks', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=4, column='L_Clicks', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=5, column='M_Clicks', value=[0.0 for i in range(df_merged.shape[0])])
            #print(df_merged.head())
            #print(df_merged.columns)

            col = df_merged.pop('Time')
            df_merged.insert(0, col.name, col)
            del df1, df2

            df = pd.merge( chair_df, df_merged, on=['Time'])
            df.drop(['Date','A0','A1','A2','A3','A4'], axis = 1, inplace = True)
            df = df.reindex(columns=column_names)
            #print(df.head())
            #print(df.columns)

            features_file = ''.join((c.split('/')[-1].split('.')[0],'.csv'))
            features_dir = get_features()
            features_file = os.path.join(features_dir,features_file)
            df.to_csv(features_file, encoding='utf-8', index=False)

        elif(k_res):
            print('Keyboard is missing')
            mf, mt, m_start = get_mouse_features(m,float(segment_size))
            cf, ct, c_start = get_chair_features(c,float(segment_size))

            print(m,'\t',c)
            tmp = ut.splitall(m)
            start_m = tmp[-1]
            print(start_m)
            start_m = start[11:-4]
            print(start_m)


            sys.exit()

            print(mf)
            print(mt)
            res1 = convert_seconds(mt)
            print(res1)
            print(len(mf), len(mt))
            print(m_start)


            print(cf)
            print(ct)
            res2 = convert_seconds(ct)
            print(res2)
            print(len(cf), len(ct))
            print(c_start)

            compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
            tmp = compare(res1, res2)
            print('Are the lists identical? :',tmp)
            #sys.exit()
            continue

            chair_df = pd.read_csv(c)
            chair_df['Time'] = chair_df['Time'].str.split(',').str[0]
            df1 = pd.DataFrame(mf, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
            df1['Time'] = convert_seconds(mt)
            df2 = pd.DataFrame(cf, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
            df2['Time'] = convert_seconds(ct)

            #REVIEW STO AGGREGATION

            data_frames = [df1, df2]
            df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Time'],how='outer'), data_frames).fillna('0.0')
            df_merged.sort_values(by='Time', inplace=True, ascending=True)

            #Add Columns
            df_merged.insert(loc=6, column='All_keys_N', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=7, column='Arrow_keys_N', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=8, column='Spaces_N', value=[0.0 for i in range(df_merged.shape[0])])
            df_merged.insert(loc=9, column='Shft_Ctrl_Alt_N', value=[0.0 for i in range(df_merged.shape[0])])
            #print(df_merged.head())
            #print(df_merged.columns)

            col = df_merged.pop('Time')
            df_merged.insert(0, col.name, col)
            del df1, df2
            df = pd.merge( chair_df, df_merged, on=['Time'])
            df.drop(['Date','A0','A1','A2','A3','A4'], axis = 1, inplace = True)
            df = df.reindex(columns=column_names)
            #print(df.head())
            #print(df.columns)

            features_file = ''.join((c.split('/')[-1].split('.')[0],'.csv'))
            features_dir = get_features()
            features_file = os.path.join(features_dir,features_file)
            df.to_csv(features_file, encoding='utf-8', index=False)

        elif (m_res == True and k_res == True):
            print('Mouse and Keyboard are missing')
            continue
            cf, ct, c_start = get_chair_features(c,float(segment_size))

            print(cf)
            print(ct)
            res = convert_seconds(ct)
            print(res)
            print(len(cf), len(ct))
            print(c_start)
            #sys.exit()
            continue

            chair_df = pd.read_csv(c)
            chair_df['Time'] = chair_df['Time'].str.split(',').str[0]
            df1 = pd.DataFrame(cf, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
            df1['Time'] = convert_seconds(ct)

            #REVIEW STO AGGREGATION

            #Add Columns
            df1.insert(loc=0, column='Velocity_X', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=1, column='Velocity_Y', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=2, column='Clicks', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=3, column='R_Clicks', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=4, column='L_Clicks', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=5, column='M_Clicks', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=6, column='All_keys_N', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=7, column='Arrow_keys_N', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=8, column='Spaces_N', value=[0.0 for i in range(df1.shape[0])])
            df1.insert(loc=9, column='Shft_Ctrl_Alt_N', value=[0.0 for i in range(df1.shape[0])])
            #print(df1.head())
            #print(df1.columns)

            col = df1.pop('Time')
            df1.insert(0, col.name, col)
            df = pd.merge( chair_df, df1, on=['Time'])
            df.drop(['Date','A0','A1','A2','A3','A4'], axis = 1, inplace = True)
            df = df.reindex(columns=column_names)
            #print(df.head())
            #print(df.columns)

            features_file = ''.join((c.split('/')[-1].split('.')[0],'.csv'))
            features_dir = get_features()
            features_file = os.path.join(features_dir,features_file)
            df.to_csv(features_file, encoding='utf-8', index=False)
        else:
            print('All files are here')
            continue
            mf, mt, m_start = get_mouse_features(m,float(segment_size))
            kf, kt, k_start = get_key_features(k,float(segment_size))
            cf, ct, c_start = get_chair_features(c,float(segment_size))

            print(kf)
            print(kt)
            res1 = convert_seconds(ct)
            print(res1)
            print(len(kf), len(kt))
            print(k_start)

            print(mf)
            print(mt)
            res2 = convert_seconds(mt)
            print(res2)
            print(len(mf), len(mt))
            print(m_start)

            print(cf)
            print(ct)
            res3 = convert_seconds(ct)
            print(res3)
            print(len(cf), len(ct))
            print(c_start)

            compare = lambda x, y, z: collections.Counter(x) == collections.Counter(y) == collections.Counter(z)
            tmp = compare(res1, res2, res3)
            print('Are the lists identical? :',tmp)
            #sys.exit()
            continue

            chair_df = pd.read_csv(c)
            chair_df['Time'] = chair_df['Time'].str.split(',').str[0]
            df1 = pd.DataFrame(mf, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
            df1['Time'] = convert_seconds(mt)
            df2 = pd.DataFrame(kf, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
            df2['Time'] = convert_seconds(kt)
            df3 = pd.DataFrame(cf, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
            df3['Time'] = convert_seconds(ct)

            #REVIEW STO AGGREGATION


            data_frames = [df1, df2, df3]
            df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Time'],how='outer'), data_frames).fillna('0.0')
            df_merged.sort_values(by='Time', inplace=True, ascending=True)
            col = df_merged.pop('Time')
            df_merged.insert(0, col.name, col)
            del df1, df2, df3
            df = pd.merge( chair_df, df_merged, on=['Time'])
            df.drop(['Date','A0','A1','A2','A3','A4'], axis = 1, inplace = True)
            df = df.reindex(columns=column_names)

            features_file = ''.join((c.split('/')[-1].split('.')[0],'.csv'))
            features_dir = get_features()
            features_file = os.path.join(features_dir,features_file)
            df.to_csv(features_file, encoding='utf-8', index=False)
'''