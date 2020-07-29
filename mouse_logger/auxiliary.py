import os
import sys
import argparse
import pandas as pd

"""
Usage: $ python3 txt_to_csv.py --fname mouselog.txt --dir /Source_path/ --dir2 /Destination_path/
"""

def convert_txt_to_csv(path,newpath,fname):
    tmp = os.path.join(path,fname)
    df = pd.read_fwf(tmp)
    fname = str(df.iloc[1,0]).replace("-","_")
    #fname = os.path.splitext(fname)[0]
    fname = fname+".csv"
    names = ["Date","Time","Action","PosX","PosY","Button"]
    newpath = os.path.join(newpath,fname)
    df.to_csv(newpath,header=names,index=False)
    return 


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Collect arguments')
    parser.add_argument("--fname", metavar='fname(text)', help="Please provide .txt log file")
    parser.add_argument("--dir", metavar='dir(text)', help="Please provide the appropriate directory")
    parser.add_argument("--dir2", metavar='dir2(text)', help="Please provide the destination directory")

    args = parser.parse_args()
    fname = args.fname
    directory = args.dir
    dest_dir = args.dir2
 
    convert_txt_to_csv(directory, dest_dir, fname)
