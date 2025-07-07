# Apollo
## An assistant for multitasking

**Apollo** is an assistant, which can help you:
- Run applications
- Search the web
- Do system actions (shutdown, restart etc.)
  
All while you are working on some task of yours.

## Tech Stack
- Python (3.13.5)
- Vosk (Speech-To-Text)
- Groq API (LLM - llama-3)
- edge-tts (Text-To-Speech)
- mpg123 (Audio playback)
  
## 🚀 Setup & Installation

Follow these steps to get **Apollo** up and running on your system:

#### Disclaimer : Built for Linux systems ( for now :| )

### 1. Clone the Repository

```bash
git clone https://github.com/RamPrakhyath05/Apollo.git
cd Apollo
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the Dependencies

```bash
pip install -r requirements.txt
```

Also install `mpg123` via your system package manager:

```bash
sudo apt install mpg123
```

*or on Arch-based systems:*

```bash
sudo pacman -S mpg123
```

### 4. Download the Vosk Model

You’ll need to manually download the Vosk small English model:

```bash
mkdir models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
cd ..
```

### 5. Set Your API Key

You’ll need a Groq API key. Set it as an environment variable:

```bash
export GROQ_API_KEY=your_key_here
```

To make this persistent, add it to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:

```bash
echo 'export GROQ_API_KEY=your_key_here' >> ~/.bashrc
```

### 6. Run Apollo 🧠🔊

```bash
python3 main.py
```

## Version History

### Apollo v1.0 (Built on and for endeavourOS - an Arch based distro)

#### Hotword Detection (Wake Word)
Continuously listens for the wake word "Apollo" using the Vosk speech recognition engine.
Uses an offline model for fast, privacy-respecting wake word detection.

#### Natural Voice Conversations
Fully voice-controlled interface. No keyboard needed, just speak.
Detects your command after the wake word, converts it to text, and sends it to the LLM.

#### Edge-TTS Integration with Streaming Playback
Streams natural-sounding voice responses using Microsoft Edge TTS (via edge-tts).
Pipes audio to mpg123 for instant playback — no saving MP3s to disk as it traditionally does.
Uses the en-GB-RyanNeural voice (but can be easily swapped for others).

#### Groq LLM Backend
Blazing-fast responses powered by llama-3.1-8b-instant from Groq API.
Markdown output is cleaned and stripped before voice synthesis, for smoother TTS.

#### Clean Async Architecture
Fully asynchronous TTS pipeline using asyncio, enabling responsive interaction.
Audio streaming and playback handled concurrently with minimal latency.

#### Zero-UI Console Mode
All terminal-driven. Ideal for low-resource systems.
