import sys
import time
import serial 
import logging
from serial import Serial
from time import sleep
from datetime import datetime

logging.basicConfig(filename="serialOut.txt",level=logging.DEBUG,format="%(asctime)s    %(message)s")
ser = serial.Serial('/dev/ttyACM0', 9600)
f = open('alekos.txt','a+')
i = 0 
flag = False

while True:
    try:        
        data_raw = str(ser.readline().decode().strip('\r\n'))
        tmp = data_raw.split('  ')[0]
        if(tmp == 'A0'):
            flag = True
        if (flag and tmp != 'A4'):
            print(data_raw) 
            logging.info(data_raw)
        if(flag and tmp == 'A4'):
            flag = False
            logging.info(data_raw)     
    except UnicodeDecodeError:
        print("UnicodeDecodeError!")
