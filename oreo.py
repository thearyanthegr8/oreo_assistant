import datetime
import os.path
import os
import time
import pyttsx3
import speech_recognition as sr
import subprocess
import pywhatkit
import random
import wikipedia
import mysql.connector
from mysql.connector import Error

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

#Put our MySQL Terminal Password
pw = "aryan0309"

#Database Name
db = "oreo"
connection = create_server_connection("localhost", "root", pw)

#Create Oreo DB
def create_database(connection, query):
    cursor = connection.cursor()
    try: 
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

create_database_query = "Create database if not exists oreo"
create_database(connection, create_database_query)

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("MySQL database connection successfull")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query was Successfull")
    except Error as err:
        print(f"Error: '{err}'")

create_user_table = """
create table if not exists users(
    username varchar(255) not null,
    password varchar(255) not null,
    name varchar(255) not null,
    age int not null,
    bot_name varchar(255)
)
"""

#Connect to the Database
connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, create_user_table)
    

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("System: Listening...")
        audio = r.listen(source)
        said = r.recognize_google(audio)

    return(said)

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

WAKE = "Oreo"


while True:
    print("Waiting for wake command")
    text = get_audio()


    if text.count(WAKE) > 0:
        speak("I am ready")
        print("I am ready")
        text = get_audio()

        GREETINGS_STRS = ["how are you", "whats up", "howdy"]
        for phrase in GREETINGS_STRS:
            if phrase in text:
                GREETINGS_REPLIES = ["I am fine, what about you?", "Everything is good", "All alright", "I am doing very well"]
                greeting = GREETINGS_REPLIES[random.randint(0, 3)]
                speak(greeting)

        NOTE_STRS = ["make a note", "write this down", "remember this", "type this"]
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("What would you like me to write down?")
                write_down = get_audio()
                note(write_down)
                speak("I've made a note of that")

        PLAYMUSIC_STRS = ["play"]
        for phrase in PLAYMUSIC_STRS:
            if phrase in text:
                text = text.replace("play", "")
                speak("Playing" + text)
                pywhatkit.playonyt(text)
                print("Oreo: Playing " + text )
                quit()

        TIME_STRS = ["tell me the time", "time", "what is the time"]
        for phrase in TIME_STRS:
            if phrase in text:
                text = text.replace(phrase, "")
                time = datetime.datetime.now().strftime('%I:%M %p')
                speak("Current time is " + time)

        SEARCH_STRS = ["what is a", "who is", "what are"]
        for phrase in SEARCH_STRS:
            if phrase in text:
                text = text.replace(phrase, "")
                result = wikipedia.summary(text, sentences=2)
                print("Oreo: Telling about " + text)
                speak(result)

        SLEEP = ["thank you", "bye"]
        for phrase in SLEEP:
            if phrase in text:
                speak("Powering down")
                print("System: Oreo left the chat")
                quit()
