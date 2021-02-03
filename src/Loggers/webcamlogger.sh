#!/bin/bash

parent_dir=`dirname \`pwd\`` #Test_Data
folder_name="/Data/Webcam" #The folder where audio and video is going to be saved
new_path=$parent_dir$folder_name

now=$(date +%F)
now="$( echo -e "$now" | tr  '-' '_'  )"
sub_dir=$new_path'/'$now

if [ -d "$sub_dir" ]; then
    echo "Date Sub-directory exists..."
    echo
else
    mkdir -p -- "$sub_dir"
    chmod 777 "$sub_dir"
    echo "Date sub-directory created..."
fi

fname=$(date +%H_%M_%S)".avi"
video_dir=$sub_dir'/'$fname
ffmpeg -f pulse -ac 1 -i default -f v4l2 -i  /dev/video0 -vcodec libx264 -t 00:01:00 $video_dir >/dev/null 2>&1 #Record for a minute and prevent ffmpeg stdout
echo "Exiting Webcamlogger"
