#!/bin/bash

end=$((SECONDS+1800))

while [ $SECONDS -lt $end ];  do
        echo 'Looping'

        #python3 chairlogger.py &
        python3 keylogger.py &
        python3 mouselogger.py

        sleep 60
done