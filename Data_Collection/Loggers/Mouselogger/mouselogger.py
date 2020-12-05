# -*- coding: utf-8 -*-
import mouse_log_functions as lf
from pynput.mouse import Listener
import logging 
import os

if __name__=='__main__':

    fname = lf.get_date()+'.txt'
    raw_data = lf.create_directories()
    fname = os.path.join(raw_data,fname)
    logging.basicConfig(filename=fname,level=logging.DEBUG,format="%(asctime)s    %(message)s")
    
    with Listener(on_move=lf.on_move, on_click=lf.on_click,on_scroll=lf.on_scroll) as listener:
        listener.join()
