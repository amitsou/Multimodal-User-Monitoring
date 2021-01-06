#!/bin/bash

#1.Creating video-audio folder
parent_dir=`dirname \`pwd\`` #Multimodal_User_Monitoring
folder_name="/Data/Webcam" #The folder where audio and video is going to be saved
new_path=$parent_dir$folder_name #Concatenating current working directory and the video audio folder

#Checkig for Webcam folder existance
if [ -d "$new_path" ]; then
    echo "video_audio folder exists..."
else
    ### Create Webcam directory ###
    #echo
    #echo "Error: ${new_path} not found..."
    #echo "Creating video_audio folder in the current directory..."
    mkdir -p -- "$new_path"
    sudo chmod 777 "$new_path"
    #echo "Folder created"
    #echo
fi

#2.Creating a sub-directory into video_audio folder
# Every sub-dir will be named based on the (current) date
now=$(date +%F) #Date needs to be formatted in YYYY-MM-DD style
now="$( echo -e "$now" | tr  '-' '_'  )" #Replacing '-' with '_'
sub_dir=$new_path'/'$now #Creating new path

#Checkig for sub-folder existance, based on date!
if [ -d "$sub_dir" ]; then
    #echo "Date Sub-directory exists..."
    echo
else
    ### Create sub-folder ###
    #echo "Error: ${sub_dir} not found..."
    #echo "Creating date sub-directory..."
    mkdir -p -- "$sub_dir"
    sudo chmod 777 "$sub_dir"
    #echo "Date sub-directory created..."
    #echo
fi


#4.Recording audio and video
fname=$(date +%H_%M_%S)".avi" #Webcam video is named based on the current time
video_dir=$sub_dir'/'$fname
ffmpeg -f pulse -ac 1 -i default -f v4l2 -i  /dev/video0 -vcodec libx264 -t 00:01:00 $video_dir #Record for a minute