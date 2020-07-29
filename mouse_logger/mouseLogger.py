import csv
import time
import logging 
import argparse
import collections
from pynput.mouse import Listener

logging.basicConfig(filename="mouselog.txt",level=logging.DEBUG,format="%(asctime)s    %(message)s")
steteOn = False
click_held = False
button = None

def on_move(x,y):
    if click_held:
        print("MV    {:5d}  {:5d}  {:5s}:".format(x,y,str(None))) 
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))
    else: 
        print("MV    {:5d}  {:5d}  {:5s}:".format(x,y,str(None))) 
        logging.info("MV    {0:>8}  {1:>8}  {2:>8}:".format(x,y,str(None)))
    
def on_click(x,y,button,pressed):
    global click_held
    if pressed:
        click_held = True
        print("CLK    {:4d}  {:5d}  {:5s}:".format(x,y,button))
        logging.info("CLK    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))
    else:
        click_held = False
        print("RLS    {:4d}  {:5d}  {:5s}:".format(x,y,button)) 
        logging.info("RLS    {0:>7}    {1:>6}    {2:>13}".format(x,y,button))

def on_scroll(x,y,dx,dy):
    if dy == -1:
        print("SCRD   {:3d}  {:5d}  {:5s}:".format(x,y,str(None))) 
        logging.info("SCRD    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    elif dy == 1:
        print("SCRU   {:3d}  {:5d}  {:5s}:".format(x,y,str(None))) 
        logging.info("SCRU    {0:>6}    {1:>6}    {2:>6}".format(x,y,str(None)))
    else:
        pass

while True:
    with Listener(on_move=on_move, on_click=on_click,on_scroll=on_scroll) as l:
        l.join()
