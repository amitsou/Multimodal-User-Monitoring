# -*- coding: utf-8 -*-
import log_functions as lf
from threading import Timer
from pynput import keyboard
import logging
import time
import os
import sys

if __name__=='__main__':

    fname = lf.get_date()+'.txt'
    raw_data = lf.create_key_log_dirs()
    fname = os.path.join(raw_data,fname)
    logging.basicConfig(filename=fname,level=logging.DEBUG,format="%(asctime)s    %(message)s")
    
    with keyboard.Listener(on_press = lf.on_press_keys) as listener:
        Timer(5, listener.stop).start()
        listener.join()