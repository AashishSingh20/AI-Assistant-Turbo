# Text-to-Speech.
import asyncio  # Used for asynchronous programming(Helps python wait for downloads, wait for speech generation, wait for network requests)
import edge_tts   # Microsoft's text to speech library
import pygame  # Here we are using it as an audio player
import os

pygame.mixer.init()

VOICE = "en-US-BrianMultilingualNeural"  

async def speak_async(text):
    Temp_Audio = "assets/temp.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(Temp_Audio)

    pygame.mixer.music.load(Temp_Audio)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

def speak(text):
    asyncio.run(speak_async(text))