# Oreo - Your personal assistant
Simple voice assistant created using Python and MySQL

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General Info
We have created a voice assistant named 'Oreo' which can be personalized slightly. One can sign in to a previous account or create a new account just by using their voice and nothing else. Once signed in, Oreo will load all of your personalized settings and then you can have it anywhere you go. Oreo is an intelligent assistant which can do a lot of work for you and make your life a little easy. When you greet Oreo it greets you back. You can ask Oreo to play a song or any video on youtube. You can ask Oreo to make some notes for you, it will note down some notes that you ask him to note. You can ask Oreo to search anything you want and give you information about the same. In the end when you are done with Oreo for the day you can ask hm to sleep. 

## Technologies
Languages used in this project are:
1. Python: Python has been the main language of this project as it makes Oreo work. From using microphone, to understanding and then replying are done by using python. We have used different modules in order to make Oreo work. 
    -We used one module of 'pywhatkit' (pywhatkit.playonyt()) to play youtube videos, music etc. 
    -We used one text-to-speech module 'pyttsx3'. In order to open notepad we used the module subprocess. 
    -We use the speech recognition module for the system to interpret the user input via microphone
    
2. SQL: SQL is the database language we are using for saving all of the user's settings such as login information, personalized settings and etc.

## Setup
To start with the setup of Oreo, we will first have to create ensure if python is installed.
In IDLE:
```
>>>python --version
```
Once python is installed, check for pip:
```
>>>pip --version
```
After verification is done, it is highly recommended to use a Virtual Environment for installation of modules. To do that:
```
pip install virtualenv
virtualenv venv
venv\scripts\activate
```
This will create and activate our Virtual Environment. First git clone this repository.<br>
Now we will have to pip install all of the required modules.
```
pip install requirements.txt
```
We will also need another module called PyAudio and since a lot of devices have issues installing it, there is an easier way. Visit this website:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio.<br>
Here use the python version and the architecture version to download the specified wheel file. Download it in the folder of your project and then pip install <filename>.<br>
After installing, just run the oreo.py file in the terminal and you are good to go😉
