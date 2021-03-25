# -*- coding: utf-8 -*-
from Functions import utils as ut
from plotly.subplots import make_subplots
from statistics import mean, stdev
from datetime import timedelta
from functools import reduce
import plotly.graph_objs as go
import plotly as py
import pandas as pd
import numpy as np
import collections
import itertools
import datetime
import shutil
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import utils as ut

#TO DO: REVIEW get_recordings()
def get_recordings():
    """Get the recorded .csv files

    Returns:
        list: A list containing the absolute dirs for the recorded .csv files
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))

    mouse = os.path.join(current_path,'Data','Mouse','CSV')
    #mouse = os.path.join(current_path,'Debug','Mouse','CSV')

    mouse_files = []
    for f in os.listdir(mouse):
        tmp = '/'.join((mouse,f))
        mouse_files.append(tmp)

    keyboard = os.path.join(current_path,'Data','Keyboard','CSV')
    #keyboard = os.path.join(current_path,'Debug','Keyboard','CSV')

    keyboard_files = []
    for f in os.listdir(keyboard):
        tmp = '/'.join((keyboard,f))
        keyboard_files.append(tmp)

    chair = os.path.join(current_path,'Data','Chair','CSV')
    #chair = os.path.join(current_path,'Debug','Chair','CSV')

    chair_files = []
    for f in os.listdir(chair):
        tmp = '/'.join((chair,f))
        chair_files.append(tmp)

    return mouse_files, keyboard_files, chair_files


def convert_seconds(seconds):
    """Convert the given seconds into hh:mm:ss format

    Args:
        seconds (float): The given seconds

    Returns:
        list: A list containing the converted seconds into time format
    """
    seconds = list(map(int,seconds))
    dt0 = datetime.datetime(1,1,1)

    time = []
    for i,t in enumerate(seconds):
        h = int(t // 3600)
        m = int(t % 3600 // 60)
        s = int(t % 3600 % 60)
        td = datetime.timedelta(hours=h, minutes=m, seconds=s)
        td = (dt0+td).strftime('%X')
        time.append(td)
    time = np.array(time)
    return time


def get_seconds(timestamp,index):
    """Convert timestamp into seconds

    Args:
        timestamp (list): A list containing the csv file timestamps
        index (int): The index where the day changes, if None there
                     is not any next day into the recorded file
    Returns:
        list: Timestamps in second format
    """

    tmp = []
    if index != None:
        tmp = [i for i,t in enumerate(timestamp) if i >= index] #save the next day indexes
        tmp1 = [t for i,t in enumerate(timestamp) if i < index]
        tmp1 = tmp1[-1].split(':') #get the last time of the previous day

        if len(tmp1) == 3:
            tmp1 = float(tmp1[0]) * 3600 + float(tmp1[1]) * 60 + float(tmp1[2].replace(',', '.'))
        else:
            print('Problem Reading Data')
            return

    times_seconds = []
    for i, t in enumerate(timestamp):
        split = t.split(':')

        if len(split) == 3:
            if i in tmp:
                seconds = float(split[0]) * 3600 + float(split[1]) * 60 + float(split[2].replace(',', '.')) + tmp1
                times_seconds.append(seconds)
            else:
                seconds = float(split[0]) * 3600 + float(split[1]) * 60 + float(split[2].replace(',', '.'))
                times_seconds.append(seconds)
        else:
            print('Problem Reading Data')
            return

    del tmp
    return times_seconds


def absoluteFilePaths(directory) -> list:
    """Get the absolute paths given a directory

    Args:
        directory (str): The directory to examine

    Returns:
        list: A list containing the file names in absolute path format
    """
    l = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
             l.append(os.path.abspath(os.path.join(dirpath, f)))
    return l


def velocity(array):
    """ Get a numpy array of mouse positions on the screen
        and calculate their average speed

    Args:
        array (floats): Mouse position on the screen

    Returns:
        numpy array: Return mouse speed
    """
    array = np.array(array)
    return np.sum(np.abs(array[1:] - array[0:-1])) / len(array)


def get_mouse_features(filename,segment_size):
    """Mouse feature extraction

    Args:
        filename (str): CSV recordings file
        segment_size (int): Create segments on the given number

    Returns:
        np.arrays: Containing the calculated features, the segment time centers and the starting day
    """

    data = pd.read_csv(filename, delimiter=',')
    times = list(data['Time'])
    x, y, b = data['PosX'], data['PosY'], data['Button']

    day_start = data['Date'][0]
    next_dates = (data['Date'] > day_start)

    if next_dates.any():
        next_dates = data.loc[next_dates]
        next_day = int(next_dates.index[0])
        times_seconds = get_seconds(times,next_day)
    else:
        next_day = None
        times_seconds = get_seconds(times,next_day)

    mouse_buttons = [
        'Button.left',
        'Button.right',
        'Button.middle'
    ]

    #start = times_seconds[0]
    tmp = ut.splitall(filename) #get the first timestamp from the filename
    tmp = tmp[-1]
    start = tmp[11:-4].split('_')
    start = float(start[0]) * 3600 + float(start[1]) * 60 + float(start[2])

    features = []
    segment_centers = []
    clicks = r_clicks = l_clicks = m_clicks = 0

    while start + segment_size < times_seconds[-1]:
        end = start + segment_size
        cur_x = [ix for i, ix in enumerate(x) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_y = [iy for i, iy in enumerate(y) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_b = [ib for i, ib in enumerate(b) if times_seconds[i] >=start and times_seconds[i] <= end]

        velocity_x = velocity(cur_x)
        velocity_y = velocity(cur_y)

        for index,button in enumerate(cur_b):
            if button == 'None':
                pass
            elif button in mouse_buttons:
                clicks += 1.0
            elif button == mouse_buttons[0]:
                l_clicks += 1.0
            elif button == mouse_buttons[1]:
                r_clicks += 1.0
            elif button == mouse_buttons[2]:
                m_clicks += 1.0

        features.append([velocity_x, velocity_y, clicks/segment_size, r_clicks/segment_size,
                         l_clicks/segment_size, m_clicks/segment_size])
        segment_centers.append(start + segment_size / 2)
        start += segment_size

    features = np.array(features)
    segment_centers = np.array(segment_centers)
    return features, segment_centers, day_start


def get_key_features(filename,segment_size):
    """Keyboard feature extraction

    Args:
        filename (str): CSV recordings file
        segment_size (int): Create segments on the given number

    Returns:
        np.arrays: Containing the calculated features, the segment time centers and the starting day
    """
    data = pd.read_csv(filename, delimiter=',')
    keys = data['Key']
    times = list(data['Time'])

    day_start = data['Date'][0]
    next_dates = (data['Date'] > day_start)

    if next_dates.any():
        next_dates = data.loc[next_dates]
        next_day = int(next_dates.index[0])
        times_seconds = get_seconds(times,next_day)
    else:
        next_day = None
        times_seconds = get_seconds(times,next_day)

    subkeys = ['Key.down','Key.up','Key.left','Key.right',
        'Key.alt','Key.alt_gr','Key.alt_r','Key.ctrl',
        'Key.ctrl_r','Key.shift','Key.shift_r','Key.backspace',
        'Key.space','Key.enter','Key.page_down','Key.page_up'
    ]

    #start = times_seconds[0]
    tmp = ut.splitall(filename)
    tmp = tmp[-1]
    start = tmp[11:-4].split('_')
    start = float(start[0]) * 3600 + float(start[1]) * 60 + float(start[2])

    features = []
    segment_centers = []
    all_keys = arrow_keys = spaces = shift_ctrl_alt = 0

    while start + segment_size < times_seconds[-1]:
        end = start + segment_size
        cur_key = [key for i, key in enumerate(keys) if times_seconds[i] >=start and times_seconds[i] <= end]

        for i,key in enumerate(cur_key):
            if key == 'None':
                pass
            elif key == subkeys[12]: #spaces
                spaces += 1.0
            elif key in subkeys: #all keys
                all_keys += 1.0
            elif key in subkeys[:4]: #arrows
                arrow_keys += 1.0
            elif key in subkeys[4:11]: #key combo
                shift_ctrl_alt += 1.0

        features.append([all_keys/segment_size, arrow_keys/segment_size,
                         spaces/segment_size, shift_ctrl_alt/segment_size])
        segment_centers.append(start + segment_size / 2)
        start += segment_size

    features = np.array(features)
    segment_centers = np.array(segment_centers)
    return features, segment_centers, day_start


def get_chair_features(filename,segment_size):
    """Chair FRS  feature extraction

    Args:
        filename (str): CSV recordings file
        segment_size (int): Create segments on the given number

    Returns:
        np.arrays: Containing the calculated features, the segment time centers and the starting day
    """
    data = pd.read_csv(filename, delimiter=',')
    times = list(data['Time'])
    a0, a1, a2, a3, a4 = data['A0'], data['A1'], data['A2'], data['A3'], data['A4']

    day_start = data['Date'][0]
    next_dates = (data['Date'] > day_start)

    if (next_dates.any()):
        next_dates = data.loc[next_dates]
        next_day = int(next_dates.index[0])
        times_seconds = get_seconds(times,next_day)
    else:
        next_day = None
        times_seconds = get_seconds(times,next_day)

    #start = times_seconds[0]
    tmp = ut.splitall(filename)
    tmp = tmp[-1]
    start = tmp[11:-4].split('_')
    start = float(start[0]) * 3600 + float(start[1]) * 60 + float(start[2])

    features = []
    segment_centers = []

    while start + segment_size < times_seconds[-1]:
        end = start + segment_size
        cur_A0 = [A0 for i, A0 in enumerate(a0) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A1 = [A1 for i, A1 in enumerate(a1) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A2 = [A2 for i, A2 in enumerate(a2) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A3 = [A3 for i, A3 in enumerate(a3) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A4 = [A4 for i, A4 in enumerate(a4) if times_seconds[i] >=start and times_seconds[i] <= end]

        if not (cur_A0 or cur_A1 or cur_A2 or cur_A3):
            features.append([0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            segment_centers.append(start + segment_size / 2)

        else:
            features.append([mean(cur_A0), stdev(cur_A0), mean(cur_A1), stdev(cur_A1),mean(cur_A2),
                            stdev(cur_A2), mean(cur_A3), stdev(cur_A3), mean(cur_A4), stdev(cur_A4)])
            segment_centers.append(start + segment_size / 2)

        start += segment_size

    return features, segment_centers, day_start


#Todo: Review get_features()
def get_features() -> str:
    """Get the features path

    Returns:
        str: The path to save the generated features
    """
    current_path = os.path.abspath(os.getcwd())

    current_path = os.path.join(current_path,'Data')
    #current_path = os.path.join(current_path,'Debug')

    features_path = os.path.join(current_path,'Features')
    return features_path


def extract_features(segment_size):
    """Extract

    Args:
        segment_size (int): Create segments of segmet_size seconds
    """
    mouse,keyboard,chair = get_recordings()
    pairs = [(i, j, k) for i in mouse for j in keyboard for k in chair if i.split('/')[-1].split('.')[0] == j.split('/')[-1].split('.')[0] == k.split('/')[-1].split('.')[0]]

    for m,k,c in pairs:

        print(m)
        print(k)
        print(c,'\n')

        kf, kt, _ = get_key_features(k,float(segment_size))
        k_segment_centers = convert_seconds(kt)

        cf, ct, _ = get_chair_features(c,float(segment_size))
        c_segment_centers = convert_seconds(ct)

        mf, mt, _ = get_mouse_features(m,float(segment_size))
        m_segment_centers = convert_seconds(mt)

        '''
        print(mf)
        print(m_segment_centers)

        print(kf)
        print(k_segment_centers)

        print(cf)
        print(c_segment_centers)
        '''

        compare = lambda x, y, z: collections.Counter(x) == collections.Counter(y) == collections.Counter(z) #compare -> bool

        if compare(k_segment_centers,c_segment_centers,m_segment_centers):
            segment_centers = c_segment_centers

            #Get the annotated labels from chair recording
            chair = pd.read_csv(c)
            chair = chair.drop(['A0','A1','A2','A3','A4'], axis = 1)

            labels = list(chair['Label'])
            dates = list(chair['Date'])

            #Drop timestamps miliseconds
            timestamps = get_seconds(list(chair['Time']),None)
            timestamps = sorted(timestamps)
            timestamps = list(convert_seconds(timestamps))

            tmp = []
            label_idxs = []
            date_idxs = []

            '''
            get the common timestamps() and their indexes
            if a timestamp does not exist in the segments list
            fill tuple with space
            '''
            [tmp.append((sec,timestamps.index(sec))) if sec in timestamps else tmp.append((sec,'')) for i,sec in enumerate(segment_centers)]

            [label_idxs.append(labels[pair[1]]) if pair[1] != '' else label_idxs.append(0) for index,pair in enumerate(tmp)] #Map the labels
            [date_idxs.append(dates[pair[1]]) if pair[1] != '' else date_idxs.append('NaN') for index,pair in enumerate(tmp)] #Map the Dates
            del tmp

            #Convert np arrays to dataframes
            df1 = pd.DataFrame(mf, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
            df2 = pd.DataFrame(kf, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
            df3 = pd.DataFrame(cf, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])

            df1['Time'] = m_segment_centers
            df2['Time'] = k_segment_centers
            df3['Time'] = c_segment_centers

            '''
            print(len(df1))
            print(len(df2))
            print(len(df3))

            print(df1,'\n')
            print(df2,'\n')
            print(df3,'\n')
            '''

            merge = df1.set_index('Time').join(df2.set_index('Time')).join(df3.set_index('Time'))
            merge.insert(loc=0, column='Date', value=date_idxs)
            merge.insert(loc=len(merge.columns), column='Label', value=label_idxs)
            merge.fillna(0.0, inplace=True)

            merge.reset_index(inplace=True)
            titles = list(merge.columns)
            titles[0], titles[1] = titles[1], titles[0]
            merge = merge[titles]

            '''
            print(merge.columns)
            print(merge.head())
            print()
            #print(len(merge))
            #print(len(date_idxs))
            #print(len(label_idxs))
            '''

            #Save to .csv file
            features_file = ''.join((c.split('/')[-1].split('.')[0],'.csv'))
            features_dir = get_features()
            features_file = os.path.join(features_dir,features_file)
            merge.to_csv(features_file, encoding='utf-8', index=False)

            del df1,df2,df3,merge



def cmp_segments(filename, segment_size):
    """Check whether the seconds segment size is greater
       than the recorded second number

    Args:
        filename (str): The recorded .csv file
        segment_size (int): A number describing how many second
                            chunks to examine
    Returns:
        bool: True or False
    """
    df = pd.read_csv(filename)
    times = list(df['Time'])
    day_start = df['Date'][0]
    next_dates = (df['Date'] > day_start)

    if next_dates.any():
        next_dates = df.loc[next_dates]
        next_day = int(next_dates.index[0])
        times_in_sec = get_seconds(times, next_day)
    else:
        next_day = None
        times_in_sec = get_seconds(times, next_day)

    start_time = times_in_sec[0]
    end_time = times_in_sec[-1]

    if start_time + float(segment_size) >= end_time:
        return True
    return False


#TO DO SET DIRECTORY!
def get_all_features():
    """Concatenate every .csv file in a directory into a bigger dataframe
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))

    f_path = os.path.join(current_path,'Data','Features','Segment_size_10')
    #f_path = os.path.join(current_path,'Debug','Features')

    abs_path = absoluteFilePaths(f_path)

    list_of_dataframes = []
    for filename in abs_path:
        list_of_dataframes.append(pd.read_csv(filename))

    merged_df = pd.concat(list_of_dataframes)
    merged_df.sort_values(by='Time', inplace=True, ascending=True)
    newDf = merged_df.dropna(how='any', subset=['Label'])
    newDf.to_csv('actions.csv',encoding='utf-8', index=False)
