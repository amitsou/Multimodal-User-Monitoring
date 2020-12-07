# -*- coding: utf-8 -*-
import pandas as pd
import logging 
import time 
import os 

click_held = False
button = None

def on_move(x,y):
    """Get the x and y coordinates of the mouse movement
    
    Parameters
    ----------
    x,y : float
        Mouse coordinates on screen
    """
    if click_held: 
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))
    else: 
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))
    
def on_click(x,y,button,pressed):
    """Get the click pressed
    
    Parameters
    ----------
    x,y : float
        Mouse coordinates on screen
    button: str
        The mouse click pressed(left or right)
    pressed: boolean
    """
    global click_held
    if pressed:
        click_held = True
        logging.info("CLK    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))
    else:
        click_held = False
        logging.info("RLS    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))

def on_scroll(x,y,dx,dy):
    """Extract the mouse scroll area 
    
    Parameters
    ----------
    x,y : float
        Mouse coordinates on screen
    dx,dy: float
        Positive or negative displacement of the scroll button
    """
    if dy == -1: 
        logging.info("SCRD    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    elif dy == 1:
        logging.info("SCRU    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    else:
        pass

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


def get_date() -> str:
    """Get the current date in order
       to properly name the recorded
       files 
        
    Returns
    -------
        The current date in YY_MM_DD format
    """
    return time.strftime('%Y_%m_%d')

def create_mouse_log_dirs() -> str:
    """Create the directory needed in order to
        save the sensor recordings
    
    Returns
    ----------
        The absolute path name of the folder
        that the raw mouse log will be saved
    """
    current_path = os.path.abspath(os.getcwd())
    current_path = os.path.join(current_path,'Loggers')
    #Create the mouse log folder
    raw_data = os.path.join(current_path,'Mouse_Raw_Data')
    if(os.path.isdir(raw_data)):
        pass
    else:
        os.mkdir(raw_data)
    #Create folder for the converted csv files
    transposed_data = os.path.join(current_path,'Mouse_CSV_Data')
    if(os.path.isdir(transposed_data)):
        pass
    else:
        os.mkdir(transposed_data)
    #Create the folder to move the edited mouse logs from 
    #the Raw_Data directory
    edited_recordings = os.path.join(current_path,'Mouse_Edited_logs')
    if(os.path.isdir(edited_recordings)):
        pass
    else:
        os.mkdir(edited_recordings)
    return raw_data

def create_key_log_dirs() -> str:
    """Create the directory needed in order to
        save the sensor recordings
    
    Returns
    ----------
        The absolute path name of the folder
        that the raw key log will be saved
    """
    current_path = os.path.abspath(os.getcwd())
    current_path = os.path.join(current_path,'Loggers')
    #Create key logger recordings folder
    raw_data = os.path.join(current_path,'Key_Raw_Data')
    if(os.path.isdir(raw_data)):
        pass
    else:
        os.mkdir(raw_data)
    #Create folder for the converted csv files
    transposed_data = os.path.join(current_path,'Key_CSV_Data')
    if(os.path.isdir(transposed_data)):
        pass
    else:
        os.mkdir(transposed_data)
    #Create the folder to move the edited key logs from 
    #the Raw_Data directory
    edited_recordings = os.path.join(current_path,'Key_Edited_logs')
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

def convert_keys2_csv(input_file,output_file):
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

def convert_mouse2_csv(input_file,output_file):
    """Convert the data stream file(keylogger recording) from .txt to .csv format

    Parameters
    ----------
    input_file : 
        The data stream file in .txt format
    output_file:
        The csv extension file name
    """    
    df = pd.read_fwf(input_file)
    col_names = ["Date","Time","Action","PosX","PosY","Button"]
    df.to_csv(output_file,header=col_names,encoding='utf-8',index=False)
