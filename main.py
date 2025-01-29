import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load API keys securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech and speak it out."""
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    """Process user command using OpenAI's GPT model."""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Pluto, skilled in general tasks like Alexa and Google Assistant. Give short responses."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I couldn't process your request."

def getNews():
    """Fetch top news headlines using NewsAPI."""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        if articles:
            for article in articles[:5]:  # Limit to 5 news items
                speak(article.get("title"))
        else:
            speak("No news articles found.")
    except requests.exceptions.RequestException as e:
        print("News API error:", e)
        speak("Sorry, I couldn't fetch the news.")

def processCommand(command):
    """Process recognized voice commands."""
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif "open chrome" in command:
        webbrowser.open("https://chrome.com")
    elif command.startswith("play "):
        song = command.split(" ", 1)[1]  # Handle multi-word song names
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the library.")
    elif "news" in command:
        getNews()
    else:
        # Let OpenAI handle the request
        response = aiProcess(command)
        speak(response)

def listenForCommand():
    """Listen for a user command after 'Pluto' is called."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Pluto Activated. Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"Recognized Command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return None
        except sr.RequestError as e:
            print(f"Speech Recognition API error: {e}")
            return None

if __name__ == "__main__":
    speak("Initializing Pluto...")
    
    while True:
        print("Listening for wake word 'Pluto'...")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adapt to background noise
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                wake_word = recognizer.recognize_google(audio).lower()
                if wake_word == "pluto":
                    speak("Yes?")
                    command = listenForCommand()
                    if command:
                        processCommand(command)
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError as e:
                print(f"Speech Recognition API error: {e}")
