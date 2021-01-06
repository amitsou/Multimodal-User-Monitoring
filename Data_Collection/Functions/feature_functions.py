# -*- coding: utf-8 -*-
from plotly.subplots import make_subplots
from statistics import mean, stdev
from datetime import timedelta
import plotly.graph_objs as go
import plotly as py
import datetime
import pandas as pd
import numpy as np
import itertools
import shutil
import time
import os
import sys



def get_recordings():
    """Get the recorded .csv files

    Returns:
        list: A list containing the absolute paths
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))

    mouse = os.path.join(current_path,'Data','Mouse','CSV')
    mouse_files = []
    for f in os.listdir(mouse):
        tmp = '/'.join((mouse,f))
        mouse_files.append(tmp)

    keyboard = os.path.join(current_path,'Data','Keyboard','CSV')
    keyboard_files = []
    for f in os.listdir(keyboard):
        tmp = '/'.join((keyboard,f))
        keyboard_files.append(tmp)

    chair = os.path.join(current_path,'Data','Chair','CSV')
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
    time = []
    dt0 = datetime.datetime(1,1,1)
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
            #get the last time of the previous day in seconds
            tmp1 = float(tmp1[0]) * 3600 + float(tmp1[1]) * 60 + float(tmp1[2].replace(',', '.'))
        else:
            print('Problem Reading Data')
            return

    times_seconds = []
    for i, t in enumerate(timestamp):
        split = t.split(':')

        if len(split)==3:
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

    if (next_dates.any()):
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

    start = times_seconds[0]
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

    if (next_dates.any()):
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

    start = times_seconds[0]
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
    """Chair FRS feature extraction

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

    start = times_seconds[0]
    features = []
    segment_centers = []

    while start + segment_size < times_seconds[-1]:
        end = start + segment_size
        cur_A0 = [A0 for i, A0 in enumerate(a0) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A1 = [A1 for i, A1 in enumerate(a1) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A2 = [A2 for i, A2 in enumerate(a2) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A3 = [A3 for i, A3 in enumerate(a3) if times_seconds[i] >=start and times_seconds[i] <= end]
        cur_A4 = [A4 for i, A4 in enumerate(a4) if times_seconds[i] >=start and times_seconds[i] <= end]
        features.append([mean(cur_A0), stdev(cur_A0), mean(cur_A1), stdev(cur_A1),mean(cur_A2),
                        stdev(cur_A2), mean(cur_A3), stdev(cur_A3), mean(cur_A4), stdev(cur_A4)])
        segment_centers.append(start + segment_size / 2)
        start += segment_size

    features = np.array(features)
    segment_centers = np.array(segment_centers)
    return features, segment_centers, day_start


def mixed_plot(f1,s1,f2,s2,f3,s3):
    """[summary]

    Args:
        f1 ([type]): [description]
        s1 ([type]): [description]
        f2 ([type]): [description]
        s2 ([type]): [description]
        f3 ([type]): [description]
        s3 ([type]): [description]
    """
    #Chair features
    df = pd.DataFrame(f1, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
    df['Time'] = s1
    #Mouse features
    df2 = pd.DataFrame(f2, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
    df2['Time'] = s2
    #Keyboard features
    df3 = pd.DataFrame(f3, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
    df3['Time'] = s3

    fig = go.Figure(data = [
            go.Scatter(x=df['Time'], y=df['M_A0'],
                name='Sensor 1 mean',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['M_A1'],
                name='Sensor 2 mean',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['STD_A0'],
                name='Sensor 1 STD',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['STD_A1'],
                name='Sensor 2 STD',
                mode='lines'),

            go.Scatter(x=df2['Time'], y=df2['Velocity_X'],
                name='Speed in X axis',
                mode='lines+markers'),

            go.Scatter(x=df2['Time'], y=df2['Velocity_Y'],
                name='Speed in Y axis',
                mode='lines+markers'),

            go.Scatter(x=df2['Time'], y=df2['Clicks'],
                name='Clicks/N',
                mode='markers'),

            go.Scatter(x=df2['Time'], y=df2['R_Clicks'],
                name='Right Clicks/N',
                mode='markers'),

            go.Scatter(x=df3['Time'], y=df3['All_keys_N'],
                name='All keys/N',
                mode='markers'),

            go.Scatter(x=df3['Time'], y=df3['Arrow_keys_N'],
                name='Arrow Keys/N',
                mode='markers')],
        layout=go.Layout(title='Mixed Modality Features',xaxis=dict(title='Time',),yaxis=dict(title='Features',)))
    py.offline.plot(fig)


def plot_all(f1,s1,f2,s2,f3,s3):
    """[summary]

    Args:
        f1 ([type]): [description]
        s1 ([type]): [description]
        f2 ([type]): [description]
        s2 ([type]): [description]
        f3 ([type]): [description]
        s3 ([type]): [description]
    """

    #Chair features
    df = pd.DataFrame(f1, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
    df['Time'] = s1
    #Mouse features
    df2 = pd.DataFrame(f2, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
    df2['Time'] = s2
    #Keyboard features
    df3 = pd.DataFrame(f3, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
    df3['Time'] = s3

    fig = make_subplots(rows=4, cols=1, vertical_spacing=0.15, subplot_titles=['Chair Mean', 'Chair Standard Deviation', 'Mouse Metrics', 'Keyboard Metrics'])
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A0'],
            name='Sensor 1 ave',
            mode='lines'),
            1,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A1'],
            name='Sensor 2 ave',
            mode='lines'),
            1,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A2'],
            name='Sensor 3 ave',
            mode='lines'),
            1,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A3'],
            name='Sensor 4 ave',
            mode='lines'),
            1,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A4'],
            name='Sensor 5 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A0'],
            name='Sensor 1 std',
            mode='markers+lines'),
            2,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A1'],
            name='Sensor 2 std',
            mode='markers+lines'),
            2,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A2'],
            name='Sensor 3 std',
            mode='markers+lines'),
            2,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A3'],
            name='Sensor 4 std',
            mode='markers+lines'),
            2,1)
    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A4'],
            name='Sensor 5 std',
            mode='markers+lines'),
            2,1)

    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['Velocity_X'],
            name='Mouse Speed in X axis',
            mode='lines+markers'),
            3,1)
    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['Velocity_Y'],
            name='Mouse Speed in Y axis',
            mode='lines+markers'),
            3,1)
    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['Clicks'],
            name='Mouse Clicks/N',
            mode='lines+markers'),
            3,1)
    fig.add_trace( go.Scatter(
            x=df2['Time'],
            y=df2['R_Clicks'],
            name='Mouse Right Clicks/N',
            mode='lines+markers'),
            3,1)
    fig.add_trace( go.Scatter(
            x=df2['Time'],
            y=df2['L_Clicks'],
            name='Mouse Left Clicks/N',
            mode='lines+markers'),
            3,1)
    fig.add_trace( go.Scatter(
            x=df2['Time'],
            y=df2['M_Clicks'],
            name='Mouse Middle Clicks/N',
            mode='lines+markers'),
            3,1)

    fig.add_trace(go.Scatter(
            x=df3['Time'],
            y=df3['All_keys_N'],
            name='Keyboard All keys/N',
            mode='lines+markers'),
            4,1)
    fig.add_trace(go.Scatter(
            x=df3['Time'],
            y=df3['Arrow_keys_N'],
            name='Keyboard Arrow Keys/N',
            mode='lines+markers'),
            4,1)
    fig.add_trace(go.Scatter(
            x=df3['Time'],
            y=df3['Spaces_N'],
            name='Keyboard Spaces/N',
            mode='lines+markers'),
            4,1)
    fig.add_trace(go.Scatter(
            x=df3['Time'],
            y=df3['Shft_Ctrl_Alt_N'],
            name='Keyboard Key Combo/N',
            mode='lines+markers'),
            4, 1)
    fig.update_layout(title_text='Chair-Mouse-Keyboard-Features', title_x=0.5,width=990, height=1100)
    py.offline.plot(fig)


def plot_mouse_features(feature,second):
    """[summary]

    Args:
        feature ([type]): [description]
        second ([type]): [description]
    """

    df = pd.DataFrame(feature, columns = ['Velocity_X','Velocity_Y','Clicks','R_Clicks','L_Clicks','M_Clicks'])
    df['Time'] = second

    fig = go.Figure(data = [
            go.Scatter(x=df['Time'], y=df['Velocity_X'],
                name='Speed in X axis',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['Velocity_Y'],
                name='Speed in Y axis',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['Clicks'],
                name='Clicks/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['R_Clicks'],
                name='Right Clicks/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['L_Clicks'],
                name='Left Clicks/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['M_Clicks'],
                name='Middle Clicks/N',
                mode='lines+markers')],
        layout=go.Layout(title='Mouse Features',xaxis=dict(title='Time',),yaxis=dict(title='Mouse Features',)))
    py.offline.plot(fig)


def plot_key_features(feature,second):
    """[summary]

    Args:
        feature ([type]): [description]
        second ([type]): [description]
    """

    df = pd.DataFrame(feature, columns = ['All_keys_N','Arrow_keys_N','Spaces_N','Shft_Ctrl_Alt_N'])
    df['Time'] = second

    fig = go.Figure(data = [
            go.Scatter(x=df['Time'], y=df['All_keys_N'],
                name='All keys/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['Arrow_keys_N'],
                name='Arrow Keys/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['Spaces_N'],
                name='Spaces/N',
                mode='lines+markers'),

            go.Scatter(x=df['Time'], y=df['Shft_Ctrl_Alt_N'],
                name='Key Combo/N',
                mode='lines+markers')],
        layout=go.Layout(title='Keyboard Features',xaxis=dict(title='Time',),yaxis=dict(title='Keyboard Features',)))
    py.offline.plot(fig)


def plot_chair_features(feature,second):
    """[summary]

    Args:
        feature ([type]): [description]
        second ([type]): [description]
    """

    df = pd.DataFrame(feature, columns = ['M_A0','STD_A0','M_A1','STD_A1','M_A2','STD_A2','M_A3','STD_A3','M_A4','STD_A4'])
    df['Time'] = second
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2, subplot_titles=['Mean', "Standard Deviation"])

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A0'],
            name='Sensor 1 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A1'],
            name='Sensor 2 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A2'],
            name='Sensor 3 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A3'],
            name='Sensor 4 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['M_A4'],
            name='Sensor 5 ave',
            mode='lines'),
            1,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A0'],
            name='Sensor 1 std',
            mode='markers+lines'),
            2,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A1'],
            name='Sensor 2 std',
            mode='markers+lines'),
            2,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A2'],
            name='Sensor 3 std',
            mode='markers+lines'),
            2,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A3'],
            name='Sensor 4 std',
            mode='markers+lines'),
            2,1)

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['STD_A4'],
            name='Sensor 5 std',
            mode='markers+lines'),
            2,1)

    fig.update_layout(title_text='Chair Sensor Mean and STD', title_x=0.5,width=1500, height=900)
    py.offline.plot(fig)