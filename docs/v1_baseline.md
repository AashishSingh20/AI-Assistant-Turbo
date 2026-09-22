# TURBO V1 FUNCTIONAL BASELINE

## V1 Final Status

TURBO V1 has completed its functional baseline testing and is now frozen.

Final V1 architecture:

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

The original V1 wake-word implementation used Google Speech Recognition
to recognize "turbo". This repeatedly produced "edible" instead of
"turbo". The issue was resolved by replacing the general-purpose
STT wake-word check with a dedicated local wake-word detector using
the pretrained AST Speech Commands model and the "marvin" keyword.

"Marvin" is used as the technical V1 wake trigger. TURBO remains the
assistant name/persona.

---

# V1 FUNCTIONAL TESTING

## V1-01 — Startup

Test:

    python main.py

Result:

PASS

Observation:

Turbo starts successfully and enters the always-listening wake-word loop.

---

## V1-02 — Wake-Word Recognition

Input:

    "Marvin"

Expected:

The local wake-word detector should detect the wake word and activate
TURBO's command-listening mode.

Actual:

The local detector successfully detected "Marvin" during repeated
tests, with observed scores including:

    0.7773
    0.8393
    0.9329
    0.9999
    1.0000

Result:

PASS

Detection method:

Local pretrained AST audio classification model:

    MIT/ast-finetuned-speech-commands-v2

Wake-word class:

    marvin

Important:

The original "Turbo" wake-word problem was caused by Google Speech
Recognition repeatedly transcribing "turbo" as "edible". That approach
was replaced for the final V1 implementation.

---

## V1-03 — Time Command

Input:

    "What's the time"

Result:

PASS

Observed:

Current time was returned correctly.

Failure boundary:

None observed.

---

## V1-04 — Date Command

Input:

    "What's the date"

Result:

PASS

Observed:

22 September 2026

Failure boundary:

None observed.

---

## V1-05 — Joke Command

Input:

    "Tell me a joke"

Result:

PASS

Observed:

A joke was generated and returned successfully.

Failure boundary:

None observed.

---

## V1-06 — Open Google

Input:

    "open google"

Expected:

Google should open in the default web browser.

Actual:

Google opened successfully.

Result:

PASS

Execution path:

User command
    ↓
commands.py
    ↓
"open google" condition
    ↓
webbrowser.open()
    ↓
Google

Notes:

This command is handled locally and does not require Gemini.

---

## V1-07 — Open YouTube

Input:

    "open youtube"

Expected:

YouTube should open in the default web browser.

Actual:

YouTube opened successfully.

Result:

PASS

Execution path:

User command
    ↓
commands.py
    ↓
"open youtube" condition
    ↓
webbrowser.open()
    ↓
YouTube

Notes:

This command is handled locally and does not require Gemini.

---

## V1-08 — Known Music Lookup

Input:

    "play fairytale"

Expected:

"fairytale" should be found in musicLibrary.music and its predefined
YouTube URL should be opened.

Actual:

The "fairytale" entry was found and the predefined YouTube URL was
opened successfully.

Result:

PASS

Execution path:

User command
    ↓
commands.py
    ↓
"play" condition
    ↓
Extract query: "fairytale"
    ↓
musicLibrary.music lookup
    ↓
Predefined YouTube URL
    ↓
webbrowser.open()

---

## V1-09 — Unknown Music Lookup

Input:

    "play something random"

Expected:

If the requested song is not present in musicLibrary.music, TURBO
should use the YouTube search fallback.

Actual:

The unknown music request was handled successfully through the
fallback path.

Result:

PASS

Failure boundary:

None observed.

---

## V1-10 — Gemini Fallback

Input:

    "what is polymorphism"

Expected:

Because the query does not match a local command, TURBO should send
it to Gemini and return the generated answer.

Actual:

Gemini successfully received the request and returned a valid
explanation.

Result:

PASS

Execution path:

User command
    ↓
commands.py
    ↓
No local command matched
    ↓
utils/ai.py
    ↓
Gemini API
    ↓
Response
    ↓
speak()

Performance observation:

Gemini API latency varied between runs. Recorded measurements included
2.86 seconds and 8.19 seconds for the API request itself.

Important:

Gemini API latency is not the complete voice round-trip latency.

---

## V1-11 — Silence After Wake Word

Test:

No speech was provided after wake-word activation.

Expected:

TURBO should handle the timeout without crashing and eventually
return to wake-word mode.

Actual:

The listener returned None after the timeout and TURBO returned to
wake-word mode.

Observed behavior:

    No response Detected.
    Listening for wake word...

After the configured retry:

    Returning to wake-word mode...

Result:

PASS

---

## V1-12 — Follow-Up Timeout Handling

Test:

Wake TURBO and provide no command.

Expected:

TURBO should provide a follow-up and give the user one additional
opportunity to speak rather than retrying indefinitely.

Actual:

The final V1 implementation uses one follow-up/retry and then exits
conversation mode if no command is received.

Result:

PASS

Conversation behavior:

    Wake word
        ↓
    "Yes, how can I help you?"
        ↓
    No response
        ↓
    Follow-up
        ↓
    One final listening attempt
        ↓
    No response
        ↓
    Return to wake-word mode

This prevents the previous infinite timeout loop.

---

## V1-13 — Exit Words

Configured exit words:

- bye
- goodbye
- stop
- exit
- that's all
- nothing
- done

Expected:

A configured exit word should end the current conversation and return
TURBO to wake-word mode.

Actual:

The exit behavior was verified during end-to-end testing. For example:

    Conversation Completed!

Result:

PASS

---

## V1-14 — Ctrl+C Shutdown

Expected:

Pressing Ctrl+C should terminate TURBO cleanly without an unhandled
traceback.

Actual:

Ctrl+C terminated TURBO correctly and displayed the shutdown message.

Result:

PASS

---

# V1 PERFORMANCE BASELINE

Performance measurements establish the baseline for comparison with
TURBO V2.

Metrics:

- STT latency
- Local command latency
- Gemini API latency
- TTS generation latency
- Total voice round-trip latency
- Local command handling percentage
- Gemini/API handling percentage
- Success/failure rate

Important:

Component latency and total user-perceived latency are measured
separately.

---

## V1 Performance — Time Command

Input:

    "what's the time"

Measured time:

    4.38 seconds

Result:

PASS

Measurement scope:

From the start of process("what's the time") until the command
completed, including TTS generation and audio playback.

Notes:

This is a local command latency measurement.

It does not include microphone capture or speech-to-text latency.

It is not the complete voice round-trip latency.

---

## V1 Performance — Open Google

Input:

    "open google"

Measured time:

    0.11 seconds

Result:

PASS

Measurement scope:

From the start of process("open google") until the command completed.

Notes:

This is a local command latency measurement.

The measurement does not include microphone capture or speech-to-text
latency.

---

## V1 Performance — Known Music Lookup

Input:

    "play fairytale"

Measured time:

    2.72 seconds

Result:

PASS

Measurement scope:

From the start of process("play fairytale") until the command
completed.

This includes the local music-library lookup, TTS generation and
audio playback, and browser-opening operation.

It does not include microphone capture or speech-to-text latency.

---

## V1 Performance — Unknown Music Lookup

Input:

    "play something random"

Measured time:

    4.36 seconds

Result:

PASS

Measurement scope:

From the start of process("play something random") until the command
completed.

This represents the unknown-music fallback path and includes TTS
generation and audio playback.

It does not include microphone capture or speech-to-text latency.

---

## V1 Performance — Joke Command

Input:

    "tell me a joke"

Measured time:

    8.07 seconds

Result:

PASS

Measurement scope:

From the start of process("tell me a joke") until the command
completed, including joke generation, TTS generation, and playback.

It does not include microphone capture or speech-to-text latency.

---

## V1 Performance — Gemini Fallback

Input:

    "what is polymorphism"

Measured Gemini API time:

    2.86 seconds

Measured total command time:

    31.13 seconds

Result:

PASS

Measurement scope:

From the start of process("what is polymorphism") until the command
completed, including Gemini API processing, response handling,
TTS generation, and audio playback.

Execution path:

    process()
        ↓
    commands.py
        ↓
    ask_ai()
        ↓
    Gemini API
        ↓
    Response
        ↓
    speak()
        ↓
    Edge TTS
        ↓
    Audio playback
        ↓
    process() completes

Notes:

The Gemini API took 2.86 seconds during this run.

The complete process() call took 31.13 seconds.

A previous Gemini API measurement was 8.19 seconds, demonstrating
that API latency can vary between requests.

This is not the complete microphone-to-response voice round-trip
latency because microphone capture and speech-to-text are not
included.

---

## V1 Performance — Speech Recognition

Input:

    "what's the time"

Recognized:

    "what's the time"

STT processing time:

    0.66 seconds

Speech capture + STT:

    3.89 seconds

Result:

PASS

Measurement scope:

Speech capture + STT measures the time from starting microphone
listening until Google Speech Recognition returns the recognized text.

STT processing time measures only the Google recognize_google()
processing portion after audio capture.

Notes:

Ambient-noise calibration was performed before the timer started and
is therefore not included in this measurement.

The measurement does not include command processing, TTS, or playback.

---

# V1 Performance — Complete Voice Round Trip

Input:

    "what's the time"

Recognized:

    "what's the time"

Speech capture + STT:

    4.16 seconds

Complete voice round trip:

    8.50 seconds

Result:

PASS

Measurement scope:

From the start of the voice test until the command completed,
including microphone capture, speech recognition, command processing,
TTS generation, and audio playback.

Execution path:

    Microphone
        ↓
    Google Speech Recognition
        ↓
    commands.py
        ↓
    Time command
        ↓
    Edge TTS
        ↓
    Audio playback
        ↓
    Completion

Notes:

This represents the user-facing time required for TURBO to listen
to the command, recognize it, process it, generate the spoken
response, and finish playback.

This is a single-run measurement.

---

# V1 Performance — Complete Voice Round-Trip Baseline

Test command:

    "what's the time"

Number of valid runs:

    4

Results:

- Run 1: 8.50 seconds
- Run 2: 8.24 seconds
- Run 3: 7.70 seconds
- Run 4: 7.33 seconds

Excluded run:

- Run 5: 11.08 seconds — excluded because the test was manually
  paused during the run.

Statistics:

- Average: 7.94 seconds
- Median: 7.97 seconds
- Minimum: 7.33 seconds
- Maximum: 8.50 seconds

Result:

PASS

Notes:

Only uninterrupted runs were included in the baseline.

The excluded run was not used because manual interruption introduced
additional time that was not representative of normal TURBO operation.

A larger number of runs will be used for the final V1 vs V2 benchmark.

---

# V1 RESOLVED DEVELOPMENT ISSUES

## Original Wake-Word Failure

Original implementation:

    Google Speech Recognition
        ↓
    Recognized text
        ↓
    Check for "turbo"

Observed:

    "turbo" → "edible"

Result:

FAIL

Resolution:

The general-purpose STT wake-word check was replaced by a dedicated
local wake-word detector using the pretrained AST Speech Commands
model.

Final V1:

    Microphone
        ↓
    Local Marvin wake-word detector
        ↓
    Google Speech Recognition
        ↓
    Command processing

Result after resolution:

PASS

---

## Ambient-Noise Calibration Instability

Development issue:

Repeatedly calibrating the microphone inside listen() caused the
energy threshold to vary significantly between listening attempts.

Resolution:

Ambient-noise calibration was moved to startup and performed once
rather than repeatedly for every command.

Result:

PASS

---

## STT Command Variation

Development issue:

Google Speech Recognition sometimes returned shorter variants such as:

    "the date"

instead of:

    "what's the date"

Resolution:

Command matching was expanded to recognize natural STT variants for
time and date requests.

Result:

PASS

---

## Music Fallback Argument

Development issue:

The YouTube fallback originally passed:

    {query}

which creates a Python set rather than a string.

Resolution:

The query is passed as:

    query

Result:

PASS

---

## Follow-Up Retry Loop

Development issue:

Using continue after a timeout caused the conversation loop to retry
indefinitely.

Resolution:

The final V1 implementation gives one follow-up opportunity and then
breaks out of the conversation loop when no response is received.

Result:

PASS

---

# V1 LIMITATIONS

1. The V1 wake trigger is "Marvin", not "Turbo", because the pretrained
   Speech Commands model provides the Marvin keyword.

2. The wake-word detector is based on a pretrained model rather than a
   custom TURBO-specific wake-word model.

3. Google Speech Recognition requires an external service for command
   transcription.

4. Gemini fallback requires an external API.

5. Voice round-trip latency includes network-dependent STT and may vary.

6. Gemini API latency can vary between requests.

7. The current V1 does not contain the hybrid local-first routing
   architecture planned for V2.

---

# V1 FREEZE

Status:

    FROZEN

Final baseline:

    Wake-word detection:
        Local pretrained AST model

    Wake trigger:
        Marvin

    Speech recognition:
        Google Speech Recognition

    Local commands:
        Time, date, browser, music, jokes

    AI fallback:
        Gemini

    Text-to-speech:
        Edge TTS

    Conversation timeout:
        One follow-up retry

    Complete voice round-trip baseline:
        Average: 7.94 seconds
        Median: 7.97 seconds
        Minimum: 7.33 seconds
        Maximum: 8.50 seconds

V1 is frozen and should not be modified while TURBO V2 is developed.

The V1 baseline will be used as the reference point for evaluating
the TURBO V2 hybrid architecture.