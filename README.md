<!-- NCDRD Logo -->
<br />
<p align="center">
  <a href="https://github.com/amitsou/Multimodal-User-Monitoring">
    <img src="https://github.com/amitsou/Multimodal-User-Monitoring/blob/master/images/logo2.jpeg" alt="Logo" width="150" height="150">
  </a>
  
  <h3 align="center">Multimodal User Monitoring</h3>
  <br />
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains the thesis code entitled: <b>'Workplace recording in order to record fatigue from work sources'</b>

This dissertation takes place within the interdepartmental program of postgraduate studies in 'Data Science' which is co-organized by the Department of Informatics and Telecommunications of the University of the Peloponnese and the Institute of Informatics and Telecommunications of the National Center for Scientific Research Demokritos (NCSRD). The purpose of this work is to create a pipeline in order to collect data from sensors which include: </br>

* Resistance-power sensors mounted on a chair 
* A common web camera with a mounted microphone
* Peripherals such as the keyborad and the mouse

After the data collection process we create the Feature Vectors in order to create a Machine Learning Pipeline. Techniques from the fields of machine learning, vision computer, audio analysis and text analysis will then be used, in order to identify how much fatigue, stress and anxiety an employee is experiencing.


<!-- GETTING STARTED -->
## Getting Started

To use the existing code you must use force resistance sensors mounted on a chair. These sensors should be connected with an Arduino UNO in order to send the data via the serial monitor (through the USB port). Don't worry if you don't own any FSR sensors. You could easily use any of the remaining code files due to the reason that every file can be executed individually.</br> 
Example: If you wish to use only one modality, f.i. say you want to run a webcamlogger in order to get the user's facial expressions every minute, it can be achieved by executing './webcamlogger.sh.'  

### Prerequisites

In order to execute the code in this repository you'll need the following installations.
* FFMPEG for Linux version: 4.2.4-1ubuntu0.1 

  ``` 
  sudo apt install ffmpeg  
  ```

* Video for linux utilities v4l-utils 
  
  ```
  sudo apt install v4l-utils
  ```
 
 * In order to execute the webcamlogger you'll need to check for the installed devices on your PC

   ```
   v4l2-ctl --list-devices   
   ```
   <!-- NCDRD Logo -->
   <br />
   <p align="center">
       <a href="https://github.com/amitsou/Multimodal-User-Monitoring">
            <img src="https://github.com/amitsou/Multimodal-User-Monitoring/blob/master/images/camera.png" alt="Logo" >
       </a>
   </p>

* pynput for python3: [https://pypi.org/project/pynput/](https://pypi.org/project/pynput/)

<!-- CONTACT -->
## Contact

Alexander Mitsou - amitsou95@gmail.com

Project Link: [https://github.com/amitsou/Multimodal-User-Monitoring](https://github.com/amitsou/Multimodal-User-Monitoring)
