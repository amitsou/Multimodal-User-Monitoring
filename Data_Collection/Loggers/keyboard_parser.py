# -*- coding: utf-8 -*-
import log_functions as lf
import shutil
import os

if __name__ == '__main__':
    
    dir1 = 'Key_Raw_Data'
    dir2 = 'Key_CSV_Data'
    dir3 = 'Key_Edited_logs'
    extension1 = '.txt'
    extension2 = '.csv'
    path = os.path.abspath(os.getcwd())
    csv_path = os.path.join(path,dir2)
    edited_recs = os.path.join(path,dir3)
    
    txt_names = lf.crawl_dir(extension1,dir1)
    csv_names = [] 
    for elem in txt_names:
        name = elem.split('/')[-1].split('.')[0]
        csv_name = name+extension2 
        tmp = os.path.join(csv_path,csv_name)
        csv_names.append(tmp)
    
    if len(txt_names) == len(csv_names):
        for i in range(len(txt_names)):
            lf.convert_keys2_csv(txt_names[i],csv_names[i])
            shutil.move(txt_names[i],edited_recs)
    else:
        pass
    
