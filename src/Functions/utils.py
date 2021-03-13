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

click_held = False
button = None


def parse_CLI():
    """CLI arguments

    Returns:
        number: The number of seconds in order to extract features
    """
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--segment_size", metavar='segment_size(int)',help="Please provide the segment size")
    args = parser.parse_args()
    segment_size = args.segment_size

    return segment_size


def on_move(x,y):
    """The callback to call when mouse move events occur

    Args:
        x (float): The new pointer position
        y (float): The new pointer poisition
    """
    if click_held:
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))
    else:
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))


def on_click(x,y,button,pressed):
    """The callback to call when a mouse button is clicked

    Args:
        x (float): Mouse coordinates on screen
        y (float): Mouse coordinates on screen
        button (str): one of the Button values
        pressed (bool): Pressed is whether the button was pressed
    """
    global click_held

    if pressed:
        click_held = True
        logging.info("CLK    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))
    else:
        click_held = False
        logging.info("RLS    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))


def on_scroll(x,y,dx,dy):
    """The callback to call when mouse scroll events occur

    Args:
        x (float): The new pointer position on screen
        y (float): The new pointer position on screen
        dx (int): The horizontal scroll. The units of scrolling is undefined
        dy (int): The vertical scroll. The units of scrolling is undefined
    """
    if dy == -1:
        logging.info("SCRD    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    elif dy == 1:
        logging.info("SCRU    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    else:
        pass


def on_press_keys(key):
    """The callback to call when a button is pressed.

    Args:
        key (str): A KeyCode,a Key or None if the key is unknown
    """
    subkeys = [
    'Key.alt','Key.alt_gr','Key.alt_r','Key.backspace',
    'Key.space','Key.ctrl','Key.ctrl_r','Key.down',
    'Key.up','Key.left','Key.right','Key.page_down',
    'Key.page_up','Key.enter','Key.shift','Key.shift_r'
    ]

    key = str(key).strip('\'')
    if key in subkeys:
        logging.info(key)
    else:
        pass


def record_chair(output_file):
    """Read the data stream coming from the serial monitor
       in order to get the sensor readings

    Args:
        output_file (str): The file name, where the data stream will be stored
    """
    serial_port = "/dev/ttyACM0"
    baud_rate = 9600
    ser = serial.Serial(serial_port,baud_rate)
    logging.basicConfig(filename=output_file,level=logging.DEBUG,format="%(asctime)s    %(message)s")

    flag = False
    start = time.time()

    while time.time() - start < 100.0:
        try:
            serial_data = str(ser.readline().decode().strip('\r\n'))
            time.sleep(0.2)
            tmp = serial_data.split('  ')[0] #Getting Sensor Id
            if tmp == 'A0':
                flag = True
            if flag and tmp != 'A4':
                #print(serial_data)
                logging.info(serial_data)
            if flag and tmp == 'A4':
                flag = False
                #print(serial_data)
                logging.info(serial_data)
        except (UnicodeDecodeError, KeyboardInterrupt) as err:
            print(err)
            print(err.args)
            sys.exit(0)


def concat_names(dir) -> str:
    """Concatenate the given folder names
       with the appropriate path

    Args:
        dir (str): The directory to create the subfolders

    Returns:
        list: The new absolute paths
    """
    raw_data = os.path.join(dir,'Raw')
    edited_data = os.path.join(dir,'Edited_logs')
    csv_data = os.path.join(dir,'CSV')
    dirs = [raw_data,edited_data,csv_data]
    return dirs


def create_subdirs(paths):
    """Create sub directories given some absolute paths

    Args:
        paths (list): A list containing the paths to be created
    """
    for index,path in enumerate(paths):
        if(os.path.isdir(path)):
            pass
        else:
            os.mkdir(path)


def round_down(num,divisor) -> int:
    """Round the number of lines contained into the recording file,
       down to the nearest multiple of the given divisor

    Args:
        num (int): The number of lines contained into the given log file
        divisor (int): The divisor in order to get tuples of divisor

    Returns:
        int: The nearest multiple of five
    """
    return num-(num%divisor)


def get_date() -> str:
    """Get the current date in order to properly name
       the recored log files
    Returns:
        str: The current date in: YY_MM_DD format
    """
    return datetime.now().strftime('%Y_%m_%d')


def get_time() -> str:
    """Get the current time in order to properly name
       the recored log files

    Returns:
        str: The current time in H_M_S format
    """
    return datetime.now().strftime('%H_%M_%S')


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def crawl_dir(target,folder) -> str:
    """Enumerate all the given files in a directory
       based on the given file extension

    Args:
        target (str): The file to search for
        folder (str): The folder to search

    Returns:
        [type]: A list containing the file names
    """
    current_path = os.path.abspath(os.getcwd())
    path = os.path.join(current_path,folder)

    file_names =[]
    for f in os.listdir(path):
        if f.endswith(target):
            fname=os.path.join(path,f)
            file_names.append(fname)
    return file_names


def check_divisor(input_file):
    """Count the file's lines

    Args:
        input_file (str): The file to count

    Returns:
        number: The nearest multiple of five
    """
    line_number = count_lines(input_file)
    rounded_line = round_down(line_number,5)
    return rounded_line


def preprocess_chair_raw_data(input_file):
    """Transpose the .txt file containing the
    chair's raw data
    Args:
        input_file (str): The .txt file to process

    Returns:
        list: A list of lists to the .csv corresponding rows
    """

    d = collections.defaultdict(list)
    tmp0,tmp1,tmp2,tmp3,tmp4 = 0,1,2,3,4
    rounded_line = check_divisor(input_file)

    with open(input_file,'r') as f1:
        lines = f1.readlines()
        for i in range(rounded_line // 5):
            Sid0 = lines[i+tmp0]
            temp = Sid0.split()
            d['Sid0'].append([temp[0],temp[1],temp[2],temp[3]])

            Sid1 = lines[i+tmp1]
            temp = Sid1.split()
            d['Sid1'].append([temp[0],temp[1],temp[2],temp[3]])

            Sid2 = lines[i+tmp2]
            temp = Sid2.split()
            d['Sid2'].append([temp[0],temp[1],temp[2],temp[3]])

            Sid3 = lines[i+tmp3]
            temp = Sid3.split()
            d['Sid3'].append([temp[0],temp[1],temp[2],temp[3]])

            Sid4 = lines[i+tmp4]
            temp = Sid4.split()
            d['Sid4'].append([temp[0],temp[1],temp[2],temp[3]])

            tmp0 += 4
            tmp1 += 4
            tmp2 += 4
            tmp3 += 4
            tmp4 += 4

    l = []
    for i in range(rounded_line // 5):
        date = d['Sid0'][i][0]
        time = d['Sid0'][i][1]
        A0_val = d['Sid0'][i][3]
        A1_val = d['Sid1'][i][3]
        A2_val = d['Sid2'][i][3]
        A3_val = d['Sid3'][i][3]
        A4_val = d['Sid4'][i][3]
        l.append([date,time,A0_val,A1_val,A2_val,A3_val,A4_val])

    return l


def convert_keys2_csv(input_file,output_file):
    """Convert the data stream file(keylogger recording) from .txt to .csv format

    Args:
        input_file (str): The data stream file in .txt format
        output_file (str): The csv extension file name
    """
    if os.stat(input_file).st_size != 0:
        df = pd.read_fwf(input_file)
        col_names = ['Date','Time','Key']
        df.to_csv(output_file,header=col_names,encoding='utf-8',index=False)


def convert_mouse2_csv(input_file,output_file):
    """Convert the data stream file(mouselogger recording) from .txt to .csv format

    Args:
        input_file (str): The data stream file in .txt format
        output_file (str): The csv extension file name
    """
    if os.stat(input_file).st_size != 0:
        df = pd.read_fwf(input_file)
        col_names = ['Date','Time','Action','PosX','PosY','Button']
        df.to_csv(output_file,header=col_names,encoding='utf-8',index=False)


def convert_chair_2_csv(input_file,output_file):
    """Convert the data stream file(chair recording)
       from .txt to .csv format

    Args:
        input_file (str): The data stream file in .txt format
        output_file (str): The csv extension file name
    """
    if os.stat(input_file).st_size != 0:
        l = preprocess_chair_raw_data(input_file)
        sensor_readings_df = pd.DataFrame.from_records(l)
        sensor_readings_df.columns = ['Date','Time','A0','A1','A2','A3','A4']
        sensor_readings_df.to_csv(output_file, encoding='utf-8', index=False)
        del l

#REVIEW
def get_dirs(modality) -> list:
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))
    #os.chdir('./Debug')
    os.chdir('./Data')
    #os.chdir('./Data_Samples')
    current_path = (os.path.abspath(os.curdir))
    current_path = os.path.join(current_path,modality)
    raw_data_path = os.path.join(current_path,'Raw')
    csv_data_path = os.path.join(current_path,'CSV')
    edited_logs_path = os.path.join(current_path,'Edited_logs')
    features_path = os.path.join(current_path,'Features')

    return raw_data_path, csv_data_path, edited_logs_path, features_path


def initialize_dirs():
    """Create the appropriate directories in order to save
       and process the collected data
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir)) #Parent folder
    current_path = os.path.join(current_path,'Data')
    create_subdirs([current_path])

    features = os.path.join(current_path,'Features')
    create_subdirs([features])

    #Create mouse log folder
    mouse = os.path.join(current_path,'Mouse')
    create_subdirs([mouse])
    #Create mouse subfolders
    names = concat_names(mouse)
    create_subdirs(names)

    #Create keyboard log  folder
    keyboard = os.path.join(current_path,'Keyboard')
    create_subdirs([keyboard])
    #Create keyboard subfolders
    names = concat_names(keyboard)
    create_subdirs(names)

    #Create the chair log folder
    chair = os.path.join(current_path,'Chair')
    create_subdirs([chair])
    #Create chair subfolders
    names = concat_names(chair)
    create_subdirs(names)

    #Create webcam log folder
    webcam = os.path.join(current_path,'Webcam')
    create_subdirs([webcam])


def get_name(modality,dest) -> str:
    """Save the recorded log into /Data/<Modality_name>/Raw

    Args:
        modality (str): The log data source
        dest(str): The folder to save the data

    Returns:
        str: The absolute path where each recording is saved
    """
    current_path = os.path.abspath(os.getcwd())
    os.chdir('..')
    current_path = (os.path.abspath(os.curdir))
    current_path = os.path.join(current_path,'Data')

    if modality == 'Chair':
        chair_path = os.path.join(current_path,modality,dest)
        return chair_path

    elif modality == 'Mouse':
        mouse_path = os.path.join(current_path,modality,dest)
        return mouse_path

    elif modality == 'Keyboard':
        keyboard_path = os.path.join(current_path,modality,dest)
        return keyboard_path


def parse_raw_data(modality):
    """Convert each modality's raw data into csv format and move
       the edited raw data into the appropriate Edited_logs folder

    Args:
        modality (str): The data source
    """
    raw_data_path, csv_data_path, edited_logs_path,_ = get_dirs(modality)

    txt_names = crawl_dir('.txt',raw_data_path)
    csv_names = []
    for elem in txt_names:
        name = elem.split('/')[-1].split('.')[0]
        csv_name = name+'.csv'
        tmp = os.path.join(csv_data_path,csv_name)
        csv_names.append(tmp)

    if modality == 'Mouse':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
                convert_mouse2_csv(txt_names[i],csv_names[i])
                add_mouse_missing_values(csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)

    elif modality == 'Keyboard':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
                convert_keys2_csv(txt_names[i],csv_names[i])
                add_key_missing_values(csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)

    elif modality == 'Chair':
        if len(txt_names) == len(csv_names):
            for i, elem in enumerate(txt_names):
                convert_chair_2_csv(txt_names[i],csv_names[i])
                add_chair_missing_values(csv_names[i])
                shutil.move(txt_names[i],edited_logs_path)


def splitall(path) -> list:
    """Split a string containing an abs path into parts

    Args:
        path (str): The abs path to the directory

    Returns:
        list: A list containing the string parts
    """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def check_empty(path) -> tuple:
    """Check if a given file does not contain any data

    Args:
        path (str): The abs path to the directory

    Returns:
        tuple: A tuple containing a bool and a message
    """
    tmp = splitall(path)
    df = pd.read_csv(path)

    if df.empty:
        if 'Keyboard' in tmp:
            msg = 'Empty Keyboard File, name:',tmp[-1]
            return True, msg
        elif 'Mouse' in tmp:
            msg = 'Empty Mouse File, name:',tmp[-1]
            return True, msg
        elif 'Chair' in tmp:
            msg = 'Empty Chair File, name:',tmp[-1]
            return True, msg
    msg = 'No empty Dataframe'
    return False, msg


def count_lines(input_file) -> int:
    """Count the lines of a given file

    Args:
        input_file (str): The file to open

    Returns:
        int: An integer that shows the line number
    """
    with open(input_file) as f:
        return sum(1 for line in f)


def list_dir(path,target):
    file_names =[]
    for f in os.listdir(path):
        if(f.endswith(target)):
            fname=os.path.join(path,f)
            file_names.append(fname)
    return file_names


def preprocess_empty():
    """Find the empty .csv files for keyboard and mouse.

       This function fills the empty files with time
       and date based on the recorded chair .csv file.

       It also fills with zero or None values the empty cells
       This function is useful for the absent class
    """
    _, chair_dir, _, _ = get_dirs('Chair')
    _, keys_dir, _, _ = get_dirs('Keyboard')
    _, mouse_dir, _, _ = get_dirs('Mouse')

    chair_files = list_dir(chair_dir,'.csv')
    key_files = list_dir(keys_dir,'.csv')
    mouse_files = list_dir(mouse_dir,'.csv')

    pairs = [(i, j, k) for i in mouse_files for j in key_files for k in chair_files if i.split('/')[-1].split('.')[0] == j.split('/')[-1].split('.')[0] == k.split('/')[-1].split('.')[0]]
    for m,k,c in pairs:
        chair_df = pd.read_csv(c)

        key_empt, _ = check_empty(k)
        mouse_empt, _ = check_empty(m)

        if key_empt:
            key_df = pd.read_csv(k)
            key_df['Date'] = chair_df['Date']
            key_df['Time'] = chair_df['Time']
            key_df['Key'] = 'None'
            key_df.to_csv(k, mode='a', header=False, index=False)
            del key_df

        if mouse_empt:
            mouse_df = pd.read_csv(m)
            mouse_df['Date'] = chair_df['Date']
            mouse_df['Time'] = chair_df['Time']
            mouse_df['PosX'] = mouse_df['PosX'].fillna(0)
            mouse_df['PosY'] = mouse_df['PosY'].fillna(0)
            mouse_df['Action'] = 'None'
            mouse_df['Button'] = 'None'
            mouse_df.to_csv(m, mode='a', header=False, index=False)
            del mouse_df


def insert_last_timestamp(filename):
    """Insert the timestamp value after the recording has terminated

    Args:
        filename (str): The file to open
    """
    #now = datetime.datetime.now()
    now = datetime.now()
    date = now.date()
    date = str(date)
    timestamp = ('{:%H:%M:%S}.{:03.0f}'.format(now.time(),now.time().microsecond/1000.0)).replace('.',',')

    with open(filename, 'a') as f:
        f.write(date)
        f.write(' ')
        f.write(timestamp)


def add_mouse_missing_values(filename):
    """Add the missing values for the last recorded timestamp

    Args:
        filename (str): The csv file to process
    """
    df = pd.read_csv(filename)
    df[['Action','Button']] = df[['Action','Button']].fillna(value='None')
    df[['PosX','PosY']] = df[['PosX','PosY']].fillna(value=0)
    df.to_csv(filename, mode='a', index = False, header=False)


def add_key_missing_values(filename):
    """Add the missing values for the last recorded timestamp

    Args:
        filename (str): The csv file to process
    """
    df = pd.read_csv(filename)
    df[['Key']] = df[['Key']].fillna(value='None')
    df.to_csv(filename, mode='a', index = False, header=False)


def add_chair_missing_values(filename):
    """Add the missing values for the last recorded timestamp

    Args:
        filename (str): The csv file to process
    """
    df = pd.read_csv(filename)
    df[['A0','A1','A2','A3','A4']] = df[['A0','A1','A2','A3','A4']].fillna(value=0)
    df.to_csv(filename, mode='a', index = False, header=False)
