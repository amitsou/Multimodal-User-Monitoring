# -*- coding: utf-8 -*-
import log_functions as lf
from threading import Timer
from pynput.mouse import Listener
import logging
import time  
import os

if __name__=='__main__':

    fname = lf.get_date()+'.txt'
    raw_data = lf.create_mouse_log_dirs()
    fname = os.path.join(raw_data,fname)
    logging.basicConfig(filename=fname,level=logging.DEBUG,format="%(asctime)s    %(message)s")
    
    with Listener(on_move=lf.on_move, on_click=lf.on_click,on_scroll=lf.on_scroll) as listener:
        Timer(60, listener.stop).start()
        listener.join()
