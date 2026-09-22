import webbrowser
import pyjokes
import musicLibrary
import pywhatkit

from speech import speak  # Here we are importing it because sometimes commands also give reply
from utils.datetime_utils import tell_time, tell_date
from utils.ai import ask_ai

def process(command):
    command = command.lower()

    if "open google" in command:  # This checks when we have open google in out command if yes the it opens goggle
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif command.startswith("play"):
        query = command.replace("play", "").strip()
        if query in musicLibrary.music:
            speak(f"Playing: {query}")
            webbrowser.open(musicLibrary.music[query])
        else:
            speak(f"Playing: {query}")
            pywhatkit.playonyt(query)

    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)

    elif (
        "what's the time" in command
        or "what is the time" in command
        or "the time" in command
        or command == "time"
    ):
        tell_time()

    elif (
        "what's the date" in command
        or "what is the date" in command
        or "the date" in command
        or command == "date"
    ):
        tell_date()

    else:
        answer = ask_ai(command)  # Stores answer from ai in answer
        speak(answer)