# -*- coding: utf-8 -*-
import logging
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


def stop_scheduler():
    print('{} Data Collection Completed, Exitting Loggers... '.format(datetime.datetime.now()))
    sys.exit()

def get_data():
    print('{} Executing scripts...'.format(datetime.datetime.now()))
    subprocess.Popen(["scripts.sh"], stdin=subprocess.PIPE)

if __name__ == '__main__':
    logging.getLogger('schedule').propagate = False #disable schedule stdout

    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--stop", metavar='stop(text)', help="Please provide end time in hh:mm:ss format")
    parser.add_argument("--m", metavar='m(text)', help="Please provide the minutes in order to execute each job")
    args = parser.parse_args()

    start_time = str(datetime.datetime.now().time()).split('.')[0]
    end_time = args.stop
    minutes = args.m
    start_h, start_m, start_s = start_time.split(':')
    end_h, end_m, end_s = end_time.split(':')
    start = datetime.time(int(start_h), int(start_m), int(start_s))
    end = datetime.time(int(end_h), int(end_m), int(end_s))

    schedule.every(int(minutes)).minutes.do(get_data)
    while True:
        if ut.time_in_range(start, end, datetime.datetime.now().time()):
            schedule.run_pending()
            time.sleep(60)
        else:
            stop_scheduler()
            current_path = os.path.abspath(os.getcwd())
            os.chdir('..')
            current_path = (os.path.abspath(os.curdir))
            current_path = os.path.join(current_path,'Parsers')
            parser = '/'.join((current_path,'csv_parser.py'))
            subprocess.run(parser, shell=True)
