# -*- coding: utf-8 -*-
from serial import Serial
import pandas as pd
import collections
import logging
import serial
import time
import sys
import csv 
import os 

def get_readings(output_file):
    """Read the data stream coming from the serial monitor 
       in order to get the sensor readings
    
    Parameters
    ----------
    output_file : str
        The file name, where the data stream will be stored
    """
    serial_port = "/dev/ttyACM0"
    baud_rate = 9600
    ser = serial.Serial(serial_port,baud_rate)
    logging.basicConfig(filename=output_file,level=logging.DEBUG,format="%(asctime)s    %(message)s")
    flag = False
    start = time.time()
    while time.time() - start < 60.0:
        try:
            serial_data = str(ser.readline().decode().strip('\r\n')) 
            time.sleep(0.2)
            tmp = serial_data.split('  ')[0] #Getting Sensor Id
            if(tmp == 'A0'):
                flag = True
            if (flag and tmp != 'A4'):
                print(serial_data) 
                logging.info(serial_data)
            if(flag and tmp == 'A4'):
                flag = False
                print(serial_data)         
                logging.info(serial_data)   
        except UnicodeDecodeError:
            print("UnicodeDecodeError!")

def convert_txt_2_csv(input_file,output_file):
    """Convert the data stream file(sensor recording) from .txt to .csv format

    Parameters
    ----------
    input_file : 
        The data stream file in .txt format
    output_file:
        The csv extension file name
    """    
    if(os.path.isfile(input_file)):
        pass
    else:
        print('Invalid working directory...')
        print('Aborting...')
        sys.exit(0)

    tmp0 = 0 
    tmp1 = 1
    tmp2 = 2
    tmp3 = 3
    tmp4 = 4

    line_number = 0
    for line in open(input_file).readlines(): 
        line_number += 1
    rounded_line = round_down(line_number,5)
    d = collections.defaultdict(list)

    with open(input_file,'r') as f1:
        lines = f1.readlines()    
        for i in range(rounded_line//5):  
            #Sensor:Analog input 0 values
            Sid0 = lines[i+tmp0]
            temp = Sid0.split()
            d['Sid0'].append([temp[0],temp[1],temp[2],temp[3]])
            #Sensor:Analog input 1 values
            Sid1 = lines[i+tmp1]
            temp = Sid1.split()
            d['Sid1'].append([temp[0],temp[1],temp[2],temp[3]])
            #Sensor:Analog input 2 values
            Sid2 = lines[i+tmp2]
            temp = Sid2.split()
            d['Sid2'].append([temp[0],temp[1],temp[2],temp[3]])
            #Sensor:Analog input 3 values
            Sid3 = lines[i+tmp3]
            temp = Sid3.split()
            d['Sid3'].append([temp[0],temp[1],temp[2],temp[3]])
            #Sensor:Analog input 4 values
            Sid4 = lines[i+tmp4]
            temp = Sid4.split()
            d['Sid4'].append([temp[0],temp[1],temp[2],temp[3]])
            
            tmp0+=4
            tmp1+=4
            tmp2+=4
            tmp3+=4
            tmp4+=4
    f1.close()

    l = []
    for i in range(rounded_line//5):
        date = d['Sid0'][i][0]
        time = d['Sid0'][i][1]
        A0_val = d['Sid0'][i][3]
        A1_val = d['Sid1'][i][3]
        A2_val = d['Sid2'][i][3]
        A3_val = d['Sid3'][i][3]
        A4_val = d['Sid4'][i][3]
        l.append([date,time,A0_val,A1_val,A2_val,A3_val,A4_val])

    sensor_readings_df = pd.DataFrame.from_records(l)
    sensor_readings_df.columns = ['Date','Time','A0','A1','A2','A3','A4']
    sensor_readings_df.to_csv(output_file, encoding='utf-8', index=False)
    del l 

def round_down(num,divisor) -> int:
    """Round the number of lines contained into the chair 
       recording file, down to the nearest multiple of five

    Parameters
    ----------
    num : int
        The number of lines contained into the sensor recordings file
    divisor: The divisor in order to get tuples of five
        
    Returns
    -------
        The nearest multiple of five
    """
    return num-(num%divisor)

def get_date() -> str:
    """Get the current date in order
       to properly name the recorded
       files 
        
    Returns
    -------
        The current date in YY_MM_DD format
    """
    return time.strftime('%Y_%m_%d')

def create_directories() -> str:
    """Create the directory needed in order to
        save the sensor recordings
    
    Returns
    ----------
        The absolute path name of the folder
        that the raw chair data will be saved
    """
    current_path = os.path.abspath(os.getcwd())
    #Create chair recordings folder
    raw_data = os.path.join(current_path,'Raw_Data')
    if(os.path.isdir(raw_data)):
        pass
    else:
        os.mkdir(raw_data)
    #Create folder for the converted csv files
    transposed_data = os.path.join(current_path,'CSV_Data')
    if(os.path.isdir(transposed_data)):
        pass
    else:
        os.mkdir(transposed_data)
    #Create the folder to move the edited txt files from 
    #the Raw_Data directory
    edited_recordings = os.path.join(current_path,'Edited_Recordings')
    if(os.path.isdir(edited_recordings)):
        pass
    else:
        os.mkdir(edited_recordings)
    return raw_data

def crawl_dir(target,folder):
    """All all the given files in a directory
       based on the given file extension

    Parameters
    ----------
    target : str
        The file to search for
     folder: str
        The folder to search

    Returns
    -------
        A list containing the file names
    """
    current_path = os.path.abspath(os.getcwd())
    path = os.path.join(current_path,folder)
    file_names =[]
    for f in os.listdir(path):
        if(f.endswith(target)):
            fname=os.path.join(path,f)
            file_names.append(fname)
    return file_names
