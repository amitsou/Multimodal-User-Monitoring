#test file

import argparse
import pandas as pd

def convert_txt_to_csv(path,newpath,fname):

    filename=
    path = 
    df = pd.read_fwf(path)

    filename = fname+".csv"
    newpath=path
    names = ["Date","Time","Action","PosX","PosY","Button"]
    df.to_csv(newpath,header=names,index=False)
    return 


