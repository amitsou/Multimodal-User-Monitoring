import sys
import time
import serial 
from time import sleep
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 9600)
f = open('alekos.txt','a+')
i = 0 
flag = False

while True:
    try:        
        data_raw = str(ser.readline().decode().strip('\r\n'))
        tmp = data_raw.split(':')[0]
        
        if(tmp == 'A0 '):
            now = datetime.now()
            flag = True
            i+=1
        print(data_raw)
        #write to file
        f.write(data_raw)
        f.write("\n")
        if(flag and tmp == 'A4 '):
            print()
            flag = False
            print(now)
            #write to file 
            f.write(str(now))
            f.write("\n")
            
    except UnicodeDecodeError:
        print("UnicodeDecodeError!")
