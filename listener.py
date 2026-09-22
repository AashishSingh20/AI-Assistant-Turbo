# Records microphone audio and converts speech into text.

import speech_recognition as sr

# ------------------------------------------------------------
# SPEECH RECOGNIZER
# ------------------------------------------------------------

# Creates the SpeechRecognition recognizer object.
# It is responsible for detecting speech and sending the
# recorded audio to Google Speech Recognition.
recognizer = sr.Recognizer()

# Initial energy threshold.
# This is only the starting value; ambient-noise calibration
# below will calculate a more suitable value for the microphone.
recognizer.energy_threshold = 350

# Amount of silence that indicates the user has finished speaking.
# 0.8 seconds means the recognizer waits for about 0.8 seconds
# of silence before considering the phrase complete.
recognizer.pause_threshold = 0.8


# ------------------------------------------------------------
# MICROPHONE CALIBRATION
# ------------------------------------------------------------

# Calibrate the microphone ONCE when Turbo starts.
#
# Previously, this calibration was performed every time
# listen() was called. That caused the energy threshold to
# change dramatically between commands.
#
# Now Turbo measures the surrounding background noise once
# and reuses the resulting threshold for subsequent commands.
with sr.Microphone() as source:

    print("Calibrating microphone...")

    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

print(
    f"Initial energy threshold: "
)

# ------------------------------------------------------------
# LISTEN FUNCTION
# ------------------------------------------------------------

def listen(timeout=4, phrase_time_limit=4):
    """
    Records one user command and converts it into text.

    timeout:
        Maximum time to wait for the user to start speaking.

    phrase_time_limit:
        Maximum duration allowed for one spoken command.

    Returns:
        Recognized text as a lowercase string,
        or None if speech was not understood/detected.
    """

    # Open the microphone.
    # The microphone is automatically released when this
    # 'with' block finishes.
    with sr.Microphone() as source:

        try:

            # Listen using the already-calibrated recognizer.
            #
            # IMPORTANT:
            # We do NOT call adjust_for_ambient_noise() here.
            # Calibration has already happened once at startup.
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        except sr.WaitTimeoutError:

            # The user did not start speaking within the
            # specified timeout period.
            print("No response Detected.")
            print("Listening for wake word...")

            return None


    # --------------------------------------------------------
    # SPEECH → TEXT
    # --------------------------------------------------------

    try:
        # Send the recorded audio to Google Speech Recognition.
        # The recognized text is returned to main.py.
        command = recognizer.recognize_google(audio)
        return command.lower()

    except sr.UnknownValueError:

        # Audio was captured, but Google could not understand
        # what the user said.
        print("Couldn't Understand")

        return None

    except sr.RequestError:
        # Google Speech Recognition could not be reached,
        # usually because of an internet/service problem.
        print("Speech Recognition Service Unavailable")

        return None