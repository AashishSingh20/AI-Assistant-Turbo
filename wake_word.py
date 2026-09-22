import torch
import librosa
import time
import sounddevice as sd
import numpy as np

from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification
)


MODEL_NAME = "MIT/ast-finetuned-speech-commands-v2"

WAKE_WORD = "marvin"
WAKE_THRESHOLD = 0.5

SAMPLE_RATE = 16000
WINDOW_SECONDS = 1.0  # Size of the audio window

SILENCE_THRESHOLD = 0.01

print("Loading wake-word model...")

feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)

model = AutoModelForAudioClassification.from_pretrained(
    MODEL_NAME
)

model.eval()

print("Wake-word model loaded.")

# Find the class ID for our wake word.
WAKE_WORD_ID = None

for idx, label in model.config.id2label.items():
    if label.lower() == WAKE_WORD:
        WAKE_WORD_ID = int(idx)
        break


if WAKE_WORD_ID is None:
    raise ValueError(
        f"Wake word '{WAKE_WORD}' was not found in the model."
    )


print(f"Wake word: {WAKE_WORD}")
print(f"Wake word class ID: {WAKE_WORD_ID}")

def record_audio():
    samples = int(SAMPLE_RATE * WINDOW_SECONDS)

    print("Listening...")

    audio = sd.rec(
        samples,
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = audio.flatten()

    return audio

def detect_wake_word():

    while True:

        audio = record_audio()

        peak_amplitude = np.max(np.abs(audio))

        # Ignore obvious silence.
        # Turbo remains active and keeps listening.
        if peak_amplitude < SILENCE_THRESHOLD:
            continue

        inputs = feature_extractor(
            audio,
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        marvin_probability = probabilities[
            0,
            WAKE_WORD_ID
        ].item()

        print(
            f"Marvin score: {marvin_probability:.4f}"
        )

        if marvin_probability >= WAKE_THRESHOLD:
            print("Wake word detected!")
            return True

if __name__ == "__main__":

    detected = detect_wake_word()

    if detected:
        print("WAKE")