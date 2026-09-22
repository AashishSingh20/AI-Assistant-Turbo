# Entry point of Turbo.
# Starts the assistant and launches the request pipeline.

import random

from listener import listen
from speech import speak
from commands import process
from wake_word import detect_wake_word


# ------------------------------------------------------------
# CONVERSATION CONTROL
# ------------------------------------------------------------

# Words that explicitly end the current conversation.
EXIT_WORDS = {
    "bye",
    "goodbye",
    "stop",
    "exit",
    "that's all",
    "nothing",
    "done"
}

# Responses used when the user doesn't immediately provide
# another command.
FOLLOW_UPS = [
    "I'm listening.",
    "Okay, "
]

# ------------------------------------------------------------
# START TURBO
# ------------------------------------------------------------

speak("Initializing Turbo.....")
print("Turbo is Ready.")

# ------------------------------------------------------------
# MAIN ASSISTANT LOOP
# ------------------------------------------------------------

try:
    while True:

        # ----------------------------------------------------
        # WAKE-WORD MODE
        # ----------------------------------------------------
        # Turbo remains here indefinitely until the wake word
        # is detected.
        wake_detected = detect_wake_word()
        if not wake_detected:
            continue


        # ----------------------------------------------------
        # CONVERSATION MODE
        # ----------------------------------------------------
        speak("Yes, how can I help you?")

        while True:
            # Listen for one command.
            command = listen(
                timeout=5,
                phrase_time_limit=5
            )

            # ------------------------------------------------
            # USER DID NOT RESPOND
            # ------------------------------------------------
            # One timeout means the conversation has ended.
            # Turbo returns to wake-word mode instead of
            # repeatedly waiting for another response.
            if command is None:
                speak(random.choice(FOLLOW_UPS))

             # Give the user one final chance
                command = listen(timeout=5, phrase_time_limit=5)

                if command is None:
                    print("Returning to wake-word mode...")
                    break
                
            # Normalize the recognized command.
            command = command.lower().strip()

            # ------------------------------------------------
            # EXIT CURRENT CONVERSATION
            # ------------------------------------------------

            if command in EXIT_WORDS:
                print("Conversation Completed!")
                speak("Conversation Completed!")
                break

            # ------------------------------------------------
            # PROCESS COMMAND
            # ------------------------------------------------

            print(command)
            process(command)

            # Ask whether the user wants another command.
            speak("Anything Else?")


# ------------------------------------------------------------
# MANUAL SHUTDOWN
# ------------------------------------------------------------

except KeyboardInterrupt:
    print("\nThank you for using Turbo!")