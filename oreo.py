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
        print("MySQL Database connection successfull")
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
        cursor.close()
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
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        print("Query was Successfull")
        cursor.close()
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor(buffered=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def remove_space(text):
    return text.replace(" ", "")

def create_new_account(name, password, age, bot_name):
    create_new = (f"insert into users values ({password}, {name}, {age}, {bot_name})")
    connection = create_db_connection("localhost", "root", pw, db)
    new_account = execute_query(connection, create_new)
    speak("Your new account has been created")
    main_project()

create_user_table = """
create table if not exists users(
    password varchar(255) not null,
    name varchar(255) not null,
    age int not null,
    bot_name varchar(255)
)
"""

#Connect to the Database
connection = create_db_connection("localhost", "root", pw, db)
connecting_to_db = execute_query(connection, create_user_table)


#Oreo features start from here
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

#Make a note in notepad
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

WAKE = "Oreo"

def main_project():
    connection = create_db_connection("localhost", "root", pw, db)
    select_usernames_passwords = "select name from users"
    results = read_query(connection, select_usernames_passwords)
    filtered_results_user = []
    for result in results:
        filtered_results_user.append(result[0])

    print(filtered_results_user)
    print("Who are you?")
    speak("Who are you?")
    username_input = get_audio()
    print("User: ", username_input.lower())
    username = (f"'{username_input.lower()}'")

    connection = create_db_connection("localhost", "root", pw, db)
    select_usernames_passwords = (f"select * from users where name = {username}")
    results = read_query(connection, select_usernames_passwords)

    if (username_input.lower() == results[0][1]):
        print(f"Hello {username}, what is your password?")
        speak(f"Hello {username}, what is your password?")

        password_input = get_audio()
        password = remove_space(password_input).lower()
        print("User: ", password)

        if password == results[0][0]:
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
        else:
            speak("Sorry incorrect passowrd, see you some other time")
    else:
        speak("Sorry couldn't find you in the database. Would you like to create a new account?")
        text = get_audio()
        if text.lower() == "yes":
            create_new_account()
        else:
            speak("Sorry to see you go. Please come back sometime")

main_project()