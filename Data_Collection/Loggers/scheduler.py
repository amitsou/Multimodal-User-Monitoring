# -*- coding: utf-8 -*-
import datetime
import schedule
import argparse
import subprocess
import sys
import time
import os
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import utils as ut


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def stop_scheduler():
    print('{} Exitting... '.format(datetime.datetime.now()))
    sys.exit()

def get_data():
    print('{} Executing scripts...'.format(datetime.datetime.now()))
    subprocess.Popen(["/home/alex/Desktop/Test_Data/Loggers/scripts.sh"], stdin=subprocess.PIPE)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--start", metavar='start(text)', help="Please provide start time in hh:mm:ss format")
    parser.add_argument("--stop", metavar='stop(text)', help="Please provide end time in hh:mm:ss format")
    parser.add_argument("--m", metavar='m(text)', help="Please provide the minutes in order to execute each job")
    args = parser.parse_args()

    start_time = args.start
    end_time = args.stop
    start_h, start_m, start_s = start_time.split(':')
    end_h, end_m, end_s = end_time.split(':')
    start = datetime.time(int(start_h), int(start_m), int(start_s))
    end = datetime.time(int(end_h), int(end_m), int(end_s))
    minutes = args.m

    schedule.every(int(minutes)).minutes.do(get_data)
    while True:
        if time_in_range(start, end, datetime.datetime.now().time()):
            schedule.run_pending()
            time.sleep(120)
        else:
            stop_scheduler()