import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pyjokes
import datetime
# pip install pocketsphinx
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com") 
    elif "open youtube" in c.lower():
       webbrowser.open("https://youtube.com")
    elif c.lower().startswith('play'):
          song = c.lower().split(' ')[1]
          link = musicLibrary.music[song]
          webbrowser.open(link)
    elif "tell me a joke" in c.lower():
          joke = pyjokes.get_joke()
          print(joke)
          speak(joke)
    elif "what is today's date" in c.lower():
        date = datetime.datetime.now().strftime("%B %d, %Y")
        print(date)
        speak(f"Today's date is {date}")
    elif "what's the time" in c.lower():
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        speak(f"The time is {time}")

    elif c.lower().startswith("search"):
        query = c.lower().replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {query}")

if __name__ == "__main__":
  speak("Initializing Turbo....")
  while True:
    # Listen for the wake word "Turbo"
    # Obtain audio from the microphone
    r = sr.Recognizer()
    
    print("recognizing...")
    try:
        with sr.Microphone() as source:
           print("Listening...")
           audio = r.listen(source,timeout=4,phrase_time_limit=4)
        word = r.recognize_google(audio)
        if(word.lower() == "turbo"):
           speak("Yes,how can I help you?")
           #Listen for command
           with sr.Microphone() as source:
               print("Turbo Active...")
               audio = r.listen(source)
               command = r.recognize_google(audio)

               processCommand(command)

    except Exception as e:
        print("Error; {0}".format(e))