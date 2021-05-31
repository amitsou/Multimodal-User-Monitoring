# -*- coding: utf-8 -*-
from threading import Timer
from pynput import keyboard
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import utils as ut

if __name__=='__main__':
    rec_file = ''.join((ut.get_date(),'_',ut.get_time(),'.txt'))
    raw_data = ut.get_name('Keyboard','Raw')
    rec_file = os.path.join(raw_data,rec_file)
    logging.basicConfig(filename=rec_file,level=logging.DEBUG,format="%(asctime)s    %(message)s")

    try:
        with keyboard.Listener(on_press = ut.on_press_keys) as listener:
            Timer(100, listener.stop).start()
            listener.join()
    except KeyboardInterrupt as err:
        print(err)
        sys.exit(0)

    ut.insert_last_timestamp(rec_file)
    print('Exiting key logger...')