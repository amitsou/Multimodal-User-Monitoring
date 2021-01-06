from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly as py
import argparse
import pandas as pd
import numpy as np
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import feature_functions as features
from Functions import utils as ut


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--segment_size", metavar='segment_size(int)',help="Please provide the segment size")
    args = parser.parse_args()
    segment_size = args.segment_size

    mouse,keyboard,chair = features.get_recordings()

    for m, k, c in zip(mouse, keyboard, chair):
        mf,mt,mstart = features.get_mouse_features(m,float(segment_size))
        mouse_seconds = features.convert_seconds(mt)
        features.plot_mouse_features(mf, mouse_seconds)
        time.sleep(1)

        kf,kt,kstart = features.get_key_features(k,float(segment_size))
        key_seconds = features.convert_seconds(kt)
        features.plot_key_features(kf, key_seconds)
        time.sleep(1)

        cf,ct,cstart = features.get_chair_features(c,float(segment_size))
        chair_seconds = features.convert_seconds(ct)
        features.plot_chair_features(cf, chair_seconds)
        time.sleep(1)

        features.plot_all(cf,chair_seconds,mf,mouse_seconds,kf,key_seconds)
        time.sleep(1)
        features.mixed_plot(cf,chair_seconds,mf,mouse_seconds,kf,key_seconds)