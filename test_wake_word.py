import librosa
import torch
import time
import statistics
from pathlib import Path
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification


MODEL_NAME = "MIT/ast-finetuned-speech-commands-v2"
WAKE_THRESHOLD = 0.5

AUDIO_DIR = Path("test_audio")
audio_files = sorted(AUDIO_DIR.glob("*.wav"))  # glob searches for files ending with wav

print("Audio files found:")
for file in audio_files:
    print(file)

print("Loading model...")

feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
print("\nFeature Extractor Configuration:")
print(feature_extractor)

model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)
print("\nModel Configuration:")
print(model.config)

print("Model loaded.")

print("Loading audio...")

def test_audio(audio_file):
    print()
    print(f"Testing: {audio_file}")

    audio, sampling_rate = librosa.load(
        audio_file,
        sr=16000,
        mono=True
    )

    print(f"Audio duration: {len(audio) / sampling_rate:.2f} seconds")

    inputs = feature_extractor(
        audio,
        sampling_rate=16000,
        return_tensors="pt"
    )

    # Warm-up inference
    with torch.no_grad():
        model(**inputs)

    # Benchmark inference
    times = []

    for i in range(10):

        start_time = time.perf_counter()

        with torch.no_grad():
            outputs = model(**inputs)

        end_time = time.perf_counter()

        inference_time = end_time - start_time
        times.append(inference_time)

    # Calculate statistics
    minimum = min(times)
    maximum = max(times)
    average = statistics.mean(times)
    median = statistics.median(times)

    # Convert logits to probabilities
    probabilities = torch.softmax(outputs.logits, dim=-1)

    # Find Marvin class ID
    marvin_id = None

    for idx, label in model.config.id2label.items():
        if label.lower() == "marvin":
            marvin_id = int(idx)
            break

    # Get Marvin probability
    marvin_probability = probabilities[0, marvin_id].item()

    if marvin_probability >= WAKE_THRESHOLD:
        decision = "WAKE"
    else:
        decision = "IGNORE"

    # Find top prediction
    predicted_id = torch.argmax(probabilities, dim=-1).item()
    predicted_label = model.config.id2label[predicted_id]
    confidence = probabilities[0, predicted_id].item()

    print(f"Top Label: {predicted_label}")
    print(f"Top Confidence: {confidence:.4f}")
    print(f"Marvin Probability: {marvin_probability:.6f}")
    print(f"Decision: {decision}")

    print("Inference:")
    print(f"  Minimum: {minimum:.3f}s")
    print(f"  Maximum: {maximum:.3f}s")
    print(f"  Average: {average:.3f}s")
    print(f"  Median:  {median:.3f}s")

for file in audio_files:
    test_audio(file)