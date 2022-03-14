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

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Mysql",
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS OREO")
mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)

print(mydb)

def authentication_login(username, password):
    pass


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
    text = get_audio()

    if text.count(WAKE) > 0:
        speak("I am ready")
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
