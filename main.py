import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi= "058628b2e03d472f8f4c4be3d0844d6b"


def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client= OpenAI(
    api_key = "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"
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses"},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return(completion.choices[0].message)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open chrome" in c.lower():
        webbrowser.open("https://chrome.com")
    elif c.lower().startswith("play") :
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r= requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=058628b2e03d472f8f4c4be3d0844d6b")
        if r.status_code == 200:
            data = r.json()
            # Extract the headlines from the r
            articles = data.get('articles', [])
            for article in articles:
                speak(article.get('title'))
    else:
        #Let OpenAI handle the request
        output= aiProcess(c)
        speak(output)
        

    

if __name__ == "__main__":
    speak("Initializing Pluto......")
    while True:
        #Listen to wake word "Pluto"
        # obtain audio from the microphone
        r = sr.Recognizer()
        print("recognizing")
        

        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source, timeout= 1, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if (word.lower()== "pluto"):
                speak("Ya")
                # listen for command
                with sr.Microphone() as source:
                    print("Pluto Activate")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                processCommand(command)
            

        except Exception as e:
            print("error; {0}".format(e))


