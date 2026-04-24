import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests 
from google import genai
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

recognizer = sr.Recognizer()
newsapi = os.getenv("NEWS_API_KEY")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song] # type: ignore
        webbrowser.open(link) 

    elif "news" in c.lower():
        r = requests.get(f"https://gnews.io/api/v4/top-headlines?country=in&lang=en&token={newsapi}")

        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            # Print the Headlines
            speak("Here are the top news headlines")
            for article in articles:
                speak(article.get('title'))
                 
        else:
            print("Error:", r.status_code)

    else: # Gemini handles the request
        print("Thinking...")
        try:
            # The syntax for the new google-genai package
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=f"You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google cloud. Give short responses. The user says: {c}"
            )
            
            print(f"Jarvis: {response.text}")
            speak(response.text)
            
        except Exception as e:
            print(f"API Error: {e}")
            speak("Sorry sir, I am having trouble connecting to the network.")
  

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    
    while True:
        # Listen for the wake word "Jarvis"
        
        # obtain audio from the microphone
        
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout= 2, phrase_time_limit=2)
            word = r.recognize_google(audio) # type: ignore
            
            if("jarvis" in word.lower()):
                speak("Ya Sir")

                # Listen for the command
                with sr.Microphone() as source:
                    print("Jarvis Active!!")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)  # type: ignore

                    processcommand(command)

        except Exception as e:
            print("Error; {0}".format(e)) 