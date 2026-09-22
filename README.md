# 🎙️ Turbo Voice Assistant

Turbo is a Python-based AI voice assistant designed to interact with users through voice commands.

The project is being developed in multiple versions. **TURBO V1** serves as the stable baseline implementation, while **TURBO V2** will introduce a hybrid local-first AI architecture.

---

## ✨ Features

### TURBO V1

- 🎤 Local wake-word detection
- 🗣️ Speech-to-text command recognition
- 🌐 Web browser control
- 🎵 YouTube music playback
- 😂 Joke generation
- 🕒 Date and time commands
- 🤖 Gemini API fallback for general queries
- 🔊 Text-to-speech using Edge TTS
- ⏱️ Follow-up conversation handling
- 🛑 Automatic timeout handling
- ❌ Voice-based exit commands
- 💻 Runs locally on the user's computer

---

## 🧠 Wake-Word Detection

The original V1 implementation used **"Turbo"** as the wake word.

During testing, Google Speech Recognition frequently interpreted the spoken word **"Turbo"** incorrectly, including transcriptions such as `"edible"`. This made traditional text-based wake-word detection unreliable.

To solve this problem, V1 uses a **local pretrained keyword-spotting model** instead of relying on speech-to-text for wake-word detection.

### Current V1 Wake Word

**Technical trigger:** `Marvin`

The assistant itself is still called **Turbo**. `"Marvin"` is only the technical wake-word used by the V1 detector.

### Wake-Word Model

- Model: `MIT/ast-finetuned-speech-commands-v2`
- Framework: Hugging Face Transformers
- Detection: Local
- Sample rate: 16 kHz
- Detection window: 1 second
- Wake threshold: approximately 0.5

This allows wake-word detection to happen locally before sending the user's actual command to speech recognition.

---

## 🏗️ V1 Architecture

The final TURBO V1 pipeline is:

    Microphone
         ↓
    Local Wake-Word Detector
         ↓
    Google Speech Recognition
         ↓
    Command Processing
         ↓
    Local Commands / Gemini Fallback
         ↓
    Edge TTS
         ↓
    Audio Playback

### Architecture Components

**1. Microphone**

Captures the user's voice input.

**2. Local Wake-Word Detector**

Continuously listens for the technical wake word and detects it locally using the pretrained speech-command model.

**3. Google Speech Recognition**

After the wake word is detected, the user's command is converted from speech to text.

**4. Command Processing**

The recognized command is checked against the available local commands.

**5. Gemini Fallback**

If the command does not match a predefined local command, it can be sent to Gemini for a general AI response.

**6. Edge TTS**

The generated response is converted into speech using Edge TTS.

**7. Audio Playback**

The generated audio is played back to the user.

---

## 🛠️ Technology Stack

### Programming Language

- Python

### Speech & AI

- SpeechRecognition
- Hugging Face Transformers
- PyTorch
- Librosa
- SoundDevice
- Edge TTS
- Google Speech Recognition
- Google Gemini API

### Voice & Audio

- Pygame
- SoundFile

### Commands & Utilities

- PyJokes
- PyWhatKit
- Webbrowser
- Datetime

---

## 📁 Project Structure

    AI_Assistant_Turbo/
    │
    ├── assets/
    │
    ├── docs/
    │   └── v1_baseline.md
    │
    ├── test_audio/
    │
    ├── utils/
    │
    ├── commands.py
    ├── listener.py
    ├── main.py
    ├── musicLibrary.py
    ├── settings.py
    ├── speech.py
    ├── test_wake_word.py
    ├── wake_word.py
    │
    └── README.md

---

## 📄 File Responsibilities

### `main.py`

Main application loop.

Responsible for:

- Starting Turbo
- Waiting for the wake word
- Processing user interaction
- Handling follow-up commands
- Handling timeouts
- Returning to wake-word detection

### `wake_word.py`

Contains the local wake-word detection system.

Responsible for:

- Loading the pretrained speech-command model
- Capturing audio
- Detecting the `Marvin` keyword
- Returning the wake-word detection result

### `listener.py`

Handles microphone input and speech recognition.

Responsible for:

- Capturing speech
- Ambient-noise calibration
- Sending audio to Google Speech Recognition
- Returning recognized text

### `commands.py`

Contains the command-processing logic.

Handles predefined commands such as:

- Time
- Date
- Jokes
- Opening websites
- Playing music
- General AI queries

### `speech.py`

Handles text-to-speech generation and audio playback using Edge TTS and Pygame.

### `musicLibrary.py`

Contains music-related data used by the music command system.

### `settings.py`

Contains project configuration such as the assistant's settings and wake-word configuration.

### `test_wake_word.py`

Used to test the local wake-word detector independently.

### `docs/v1_baseline.md`

Contains the V1 testing results, performance measurements, resolved issues, limitations, and baseline documentation.

---

## ⚙️ Installation

### 1. Clone the Repository

Clone the repository to your local machine and open the project directory.

### 2. Create a Virtual Environment

    python -m venv .venv

### 3. Activate the Virtual Environment

Windows:

    .venv\Scripts\activate

Linux/macOS:

    source .venv/bin/activate

### 4. Install Dependencies

Install the required Python packages used by the project.

The exact dependency list should match the project's environment and configuration.

### 5. Configure API Access

If Gemini fallback is being used, configure the required Gemini API credentials in the project's environment configuration.

Do not commit API keys or other secrets to GitHub.

---

## ▶️ Running Turbo

Start the assistant with:

    python main.py

Once started, Turbo waits for the local wake-word detector to detect:

    Marvin

After the wake word is detected, speak the desired command.

---

## 🎤 Supported Commands

### Time

Examples:

    What time is it?
    Tell me the time.

### Date

Examples:

    What is the date?
    What's the date?

### Jokes

Examples:

    Tell me a joke.
    Make me laugh.

### Websites

Examples:

    Open Google.
    Open YouTube.

### Music

Examples:

    Play [song name].

### General Questions

Questions that are not handled by predefined local commands can be passed to the Gemini API.

---

## ⏱️ V1 Performance Baseline

The following measurements were obtained during V1 testing.

| Metric | Result |
|---|---:|
| Time command processing | 4.38 s |
| Open Google | 0.11 s |
| Known music lookup | 2.72 s |
| Unknown music lookup | 4.36 s |
| Joke command | 8.07 s |
| Gemini API response | 2.86 s |
| Speech capture + STT | 3.89 s |
| Complete voice round trip | 8.50 s |
| Average complete voice round trip | **7.94 s** |
| Median complete voice round trip | **7.97 s** |
| Minimum complete voice round trip | **7.33 s** |
| Maximum complete voice round trip | **8.50 s** |

The complete voice round-trip measurement represents the time involved in the voice interaction pipeline, from speech capture through processing and response playback.

---

## 🧪 V1 Testing

The following V1 functionality was tested:

- Startup
- Wake-word detection
- Time command
- Date command
- Joke command
- Browser commands
- Music commands
- Gemini fallback
- Silence after wake word
- Follow-up timeout handling
- Exit commands
- Ctrl+C shutdown
- Complete voice round-trip latency

### Test Result

The final V1 test cycle passed the required baseline functionality.

An occasional Google Speech Recognition `"Couldn't Understand"` response was observed during testing, but it was handled by the system and did not prevent the V1 baseline from being frozen.

---

## ⚠️ Limitations

- The V1 wake-word detector uses **"Marvin"** as the technical trigger word because the original `"Turbo"` wake word was frequently misrecognized by Google Speech Recognition.
- The wake-word detector is based on a pretrained speech-command model and is not specifically trained for the Turbo wake word.
- Speech recognition depends on microphone quality, background noise, and internet connectivity.
- Google Speech Recognition requires an internet connection for command transcription.
- Gemini-based responses require an internet connection and may be affected by API availability or quota limitations.
- V1 does not contain a learned intent-routing system.
- Command handling is primarily based on predefined command logic with Gemini used as a fallback.
- The complete voice interaction has an average measured round-trip latency of approximately **7.94 seconds**.
- V1 is a baseline architecture and does not yet contain the hybrid local-first routing planned for V2.

---

## 🚀 Future Improvements

### TURBO V2 — Hybrid Local-First Assistant

The next major version of Turbo will introduce a hybrid architecture designed to process as much work locally as possible.

Planned improvements include:

- Add a local LLM using Ollama.
- Introduce a Hybrid Router.
- Route requests between:
  - Local Tools
  - Local AI
  - External API AI
- Train a lightweight routing classifier using real user queries.
- Evaluate the router using:
  - Accuracy
  - Precision
  - Recall
  - Confusion Matrix
- Implement API fallback when the local model cannot provide a suitable response.
- Measure local and API response latency.
- Measure the percentage of queries handled locally.
- Measure complete voice round-trip latency.
- Reduce unnecessary network requests.
- Improve privacy by processing suitable requests locally.

### TURBO V2 — Improved Wake Word

A future version will also introduce a dedicated Turbo wake-word detector.

Planned improvements include:

- Collect a dedicated `"Turbo"` wake-word dataset.
- Record multiple speakers.
- Include different environmental conditions.
- Generate negative samples.
- Extract MFCC or Mel-spectrogram features.
- Train a lightweight CNN-based wake-word classifier.
- Perform proper training, validation, and testing.
- Measure:
  - Accuracy
  - Precision
  - Recall
  - False positives
  - False negatives
  - Detection latency
  - Noise robustness
- Optimize the model for local/edge execution.

---

## 📌 Project Status

### TURBO V1 — FROZEN

TURBO V1 has been:

- Implemented
- Tested
- Performance measured
- Documented
- Pushed to GitHub

The final V1 provides a stable baseline for further development.

The V1 implementation will **not be modified during V2 development**.

Future architectural development will take place in **TURBO V2**, which will introduce the hybrid local-first AI architecture.

---

## 🔮 Development Roadmap

    V1 — Baseline Voice Assistant
             ↓
    V1 Testing & Performance Measurement
             ↓
    V1 Frozen
             ↓
    V2 Hybrid Architecture
             ↓
    Local AI Integration
             ↓
    Hybrid Router
             ↓
    Routing Classifier
             ↓
    Performance Evaluation
             ↓
    Improved Turbo Wake Word
             ↓
    Public Model / Demo

---

## 🤝 Contributing

Contributions and suggestions are welcome.

If you want to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make and test your changes.
4. Commit your changes with a clear commit message.
5. Open a pull request.

For major architectural changes, discuss the proposed change before modifying the frozen V1 implementation.

---

## 📜 License

This project is intended for educational, development, and research purposes.

---

## 👨‍💻 Author

**Aashish Singh**

Computer Science Engineering  
G. H. Raisoni College of Engineering and Management, Pune

---

## ⭐ Project Note

TURBO V1 represents the baseline implementation of the assistant.

The primary development direction of the project is **TURBO V2 — a hybrid local-first AI assistant designed to perform suitable tasks locally while retaining external AI APIs as a fallback.**
