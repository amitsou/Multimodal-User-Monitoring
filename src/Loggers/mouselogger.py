# -*- coding: utf-8 -*-
from threading import Timer
from pynput.mouse import Listener
import logging
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "../"))
from Functions import utils as ut

if __name__=='__main__':
    t = time.localtime()
    print("time.asctime(t): %s " % time.asctime(t))

    rec_file = ''.join((ut.get_date(),'_',ut.get_time(),'.txt'))
    raw_data = ut.get_name('Mouse','Raw')
    rec_file = os.path.join(raw_data,rec_file)
    logging.basicConfig(filename=rec_file,level=logging.DEBUG,format="%(asctime)s    %(message)s")

    try:
        with Listener(on_move=ut.on_move, on_click=ut.on_click,on_scroll=ut.on_scroll) as listener:
            Timer(60, listener.stop).start()
            listener.join()
    except KeyboardInterrupt as err:
        print(err)
        sys.exit(0)

    ut.insert_last_timestamp(rec_file)
    print('Exiting mouse logger...')