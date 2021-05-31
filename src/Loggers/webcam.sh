#!/bin/bash

dependencies(){
    #ffmpeg installation
    package_name="ffmpeg"
    dpkg -s $package_name &> /dev/null

    if [ $? -ne 0 ]; then
        echo
        while true;
        do
            echo "Answer with y for yes or n for no."
            read -p "Do you want to install this program?:" yn
            case $yn in
                [Yy]* )
                        sudo apt-get update
                        if sudo apt-get install $package_name; then
                            echo "Successfully installed $package_name"
                        else
                            echo "Error installing $package_name"
                        fi
                        break;;
                [Nn]* )
                        exit;;
            esac
        done
    else
        echo "Package $package_name is already installed..."
    fi

    #v4l-utils :video for linux utilities installation
    package_name2="v4l-utils"
    dpkg -s $package_name2 &> /dev/null

    if [ $? -ne 0 ]; then
        echo
        while true;
        do
            echo "Answer with y for yes or n for no."
            read -p "Do you want to install this program?:" yn
            case $yn in
                [Yy]* )
                        sudo apt-get update
                        if sudo apt install $package_name2; then
                            echo "Successfully installed $package_name2"
                        else
                            echo "Error installing $package_name2"
                        fi
                        break;;
                [Nn]* )
                        exit;;
            esac
        done
    else
        echo "Package $package_name2 is already installed..."
    fi
    echo
}


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
    #sudo chmod 777 "$new_path"
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
    #sudo chmod 777 "$sub_dir"
    #echo "Date sub-directory created..."
    #echo
fi

#3.Installing the appropriate libraries
#dependencies

#4.Recording audio and video
fname=$(date +%H_%M_%S)".avi" #Webcam video is named based on the current time
video_dir=$sub_dir'/'$fname
ffmpeg -f pulse -ac 1 -i default -f v4l2 -i  /dev/video0 -vcodec libx264 -t 00:01:00 $video_dir #Record for a minute

#In order to run this script multiple times without using Crontab read the following as mentioned:
#For instance: If you wish to record videos of 10 minutes every 2 minutes, uncomment the following section
#Change seconds number to: 3600*hours_worked
#i.e. If hours_worked=8, then record 10min videos for 8 hours
#8 hours = 3600(sed per hour)*8(hours) = 28.800 seconds
#end=$((SECONDS+120))
#while [ $SECONDS -lt $end ];
#do
    #Current time in Hour_Minutes_Seconds.avi format
#    fname=$(date +%H_%M_%S)".avi"
#    video_dir=$sub_dir'/'$fname
#    ffmpeg -f pulse -ac 1 -i default -f v4l2 -i  /dev/video0 -vcodec libx264 -t 00:10:00 $video_dir
#    chmod 777 $video_dir
#done