# -*- coding: utf-8 -*-
import pandas as pd
import logging
import time 
import os 

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
        that the raw key log will be saved
    """
    current_path = os.path.abspath(os.getcwd())
    #Create key logger recordings folder
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
    #Create the folder to move the edited key logs from 
    #the Raw_Data directory
    edited_recordings = os.path.join(current_path,'Edited_logs')
    if(os.path.isdir(edited_recordings)):
        pass
    else:
        os.mkdir(edited_recordings)
    return raw_data

def on_press_keys(key):
    """Extract and save the specified key identifiers

    Parameters
    ----------
    key : str
        The id of the key pressed
    """
    subkeys = [
    'Key.alt','Key.alt_gr','Key.alt_r','Key.backspace',
    'Key.space','Key.ctrl','Key.ctrl_r','Key.down',
    'Key.up','Key.left','Key.right','Key.page_down', 
    'Key.page_up','Key.enter','Key.shift','Key.shift_r'
    ]

    key = str(key).strip('\'')
    if(key in subkeys):
        #print(key)
        logging.info(key)   
    else:
        pass

def convert_txt_2_csv(input_file,output_file):
    """Convert the data stream file(keylogger recording) from .txt to .csv format

    Parameters
    ----------
    input_file : 
        The data stream file in .txt format
    output_file:
        The csv extension file name
    """    
    df = pd.read_fwf(input_file)
    col_names = ['Date','Time','Key']
    df.to_csv(output_file,header=col_names,encoding='utf-8',index=False)

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
    
