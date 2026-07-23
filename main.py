from listener import listen  # Imports listen function from listener file 
from speech import speak   # Imports speech function from speak file
from commands import process  # imports commands function from process file
from config import WAKE_WORD  # imports WAKE_WORD from config file(If required the name of the assistant can be changed easily)
import time

print("Initializing Turbo.....")
print("Turbo is Ready.") 

while True:  # This is required so that turbo keeps on listening infinitely and not stop after executing only one command

    print("Listening...")
    word = listen()  # This will call listen command from listener and store it in word
    print("Wake Word:", word)  # Prints the word

    if word and WAKE_WORD in word.lower():  # If the Wake_word is called then speak the next line
        speak("Yes, how can I help you?")  
        command = listen(timeout=5, phrase_time_limit=5)  # This listen captures the actual command(wait for 5 sec for the user to start speaking, and record only 5 seconds)

        if(command == None):  # If command received is none then continue the conversation starting with waiting for wake word
            continue

        print(command)
        process(command)