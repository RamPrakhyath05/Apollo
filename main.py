import os
import re
import json
import asyncio
import subprocess
import pyaudio
from vosk import Model, KaldiRecognizer
from groq import Groq
import edge_tts

# === CONFIG ===
WAKE_WORD = "apollo"
VOSK_MODEL_PATH = "models/vosk-model-small-en-us-0.15"

# Silence Vosk logs
os.environ["KALDI_LOG_LEVEL"] = "ERROR"

# Load LLM + Speech Recognition models
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
model = Model(VOSK_MODEL_PATH)

# === MARKDOWN CLEANER ===
def strip_markdown(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'#+ ', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'>\s+', '', text)
    text = re.sub(r'- ', '', text)
    return text.strip()

# === AUDIO INPUT ===
def create_stream():
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    return stream

def wait_for_wake_word():
    recognizer = KaldiRecognizer(model, 16000)
    stream = create_stream()
    print("Waiting for wake word 'Apollo'...")

    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower().strip()
            if WAKE_WORD in text:
                print("Wake word detected!")
                break

    stream.stop_stream()
    stream.close()

def listen_for_command():
    recognizer = KaldiRecognizer(model, 16000)
    stream = create_stream()
    print("Listening for your command...")

    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").strip()
            stream.stop_stream()
            stream.close()
            return command

# === TTS WITH EDGE + MPG123 STREAMING ===
async def speak_async(text):
    try:
        tts = edge_tts.Communicate(text, voice="en-GB-RyanNeural")

        # Start mpg123 as a subprocess that accepts audio from stdin
        mpg123 = subprocess.Popen(
            ["mpg123", "-q", "-"],  # -q = quiet, "-" = stdin
            stdin=subprocess.PIPE
        )

        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                mpg123.stdin.write(chunk["data"])
        mpg123.stdin.close()
        mpg123.wait()

    except Exception as e:
        print(f"Edge TTS error: {e}")

def speak(text):
    print(f"Apollo says: {text}")
    asyncio.run(speak_async(text))

# === MAIN LOOP ===
def main():
    while True:
        wait_for_wake_word()
        command = listen_for_command()

        if not command:
            speak("No input detected.")
            print("⚠️ No input detected.")
            continue

        print(f"You said: {command}")

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": command}
                ],
                model="llama-3.1-8b-instant"
            )
            reply = strip_markdown(chat_completion.choices[0].message.content)
            speak(reply)
        except Exception as e:
            print(f"Groq Error: {e}")
            speak("I'm having trouble responding right now.")

if __name__ == "__main__":
    main()
