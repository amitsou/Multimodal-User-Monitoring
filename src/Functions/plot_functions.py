# -*- coding: utf-8 -*-
from Functions import feature_functions as ft
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly as py
import pandas as pd
import numpy as np
import time
import os
import sys


def plot_all(f1,s1,f2,s2,f3,s3):
    """Plot all the features

    Args:
        f1 (list): feature vector
        s1 (list): datetime seconds
        f2 (list): feature vector
        s2 (list): datetime seconds
        f3 (list): feature vector
        s3 (list): datetime seconds
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
    """Plot mouse features

    Args:
        feature (list): Modality's features
        second (datetime obj): Datetime seconds
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
    """Plot keyboard features

    Args:
        feature (list): Modality's features
        second (datetime obj): Datetime seconds
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
    """Plot chair features

    Args:
        feature (list): Modality's features
        second (datetime obj): Datetime seconds
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


def plot_raw_chair(filename):
    """Plot chair's raw data

    Args:
        filename: The .csv file to open
    """

    df = pd.read_csv(filename)
    df.drop('Date', axis =1, inplace = True)

    fig = go.Figure(data = [
            go.Scatter(x=df['Time'], y=df['A0'],
                name='Sensor 1',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['A1'],
                name='Sensor 2',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['A2'],
                name='Sensor 3',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['A3'],
                name='Sensor 4',
                mode='lines'),

            go.Scatter(x=df['Time'], y=df['A4'],
                name='Sensor 5',
                mode='lines')],
        layout=go.Layout(title='Chair Raw Data',xaxis=dict(title='Time',),yaxis=dict(title='Keyboard Features',)))
    py.offline.plot(fig)


def plot_all_raw(f1,f2,f3):
    """Plot raw recordings

    Args:
        f1 (str): Modality's Filename 1
        f2 (str): Modality's Filename 2
        f3 (str): Modality's Filename 3
    """

    df = pd.read_csv(f1)
    df.drop('Date', axis = 1, inplace = True)

    df1 = pd.read_csv(f2)
    df1.drop('Date', axis = 1, inplace = True)

    df2 = pd.read_csv(f3)
    df2.drop('Date', axis = 1, inplace = True)

    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.15,
        subplot_titles=['Chair Raw', 'Keyboard Raw', 'Mouse Raw'])

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['A0'],
            name='Sensor 1',
            mode='lines'),
            1,1),

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['A1'],
            name='Sensor 2',
            mode='lines'),
            1,1),

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['A2'],
            name='Sensor 3',
            mode='lines'),
            1,1),

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['A3'],
            name='Sensor 4',
            mode='lines'),
            1,1),

    fig.add_trace(go.Scatter(
            x=df['Time'],
            y=df['A4'],
            name='Sensor 5',
            mode='lines'),
            1,1),

    fig.add_trace(go.Scatter(
            x=df1['Time'],
            y=df1['Key'],
            name='Keys',
            mode='lines'),
            2,1),

    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['PosX'],
            name='Mouse X Position',
            mode='lines'),
            3,1),

    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['PosY'],
            name='Mouse Y Position',
            mode='lines'),
            3,1),

    fig.add_trace(go.Scatter(
            x=df2['Time'],
            y=df2['Button'],
            name='Mouse Buttons',
            mode='lines'),
            3,1),

    fig.update_layout(title_text='Chair-Mouse-Keyboard-Features',
                      title_x=0.5,width=990, height=1100)
    py.offline.plot(fig)


def plot_features(segment_size):
    mouse,keyboard,chair = ft.get_recordings()
    for m, k, c in zip(mouse, keyboard, chair):
        mf,mt,mstart = ft.get_mouse_features(m,float(segment_size))
        mouse_seconds = ft.convert_seconds(mt)
        plot_mouse_features(mf, mouse_seconds)
        time.sleep(1)

        kf,kt,kstart = ft.get_key_features(k,float(segment_size))
        key_seconds = ft.convert_seconds(kt)
        plot_key_features(kf, key_seconds)
        time.sleep(1)

        cf,ct,cstart = ft.get_chair_features(c,float(segment_size))
        chair_seconds = ft.convert_seconds(ct)
        plot_chair_features(cf, chair_seconds)
        time.sleep(1)

        plot_all(cf,chair_seconds,mf,mouse_seconds,kf,key_seconds)