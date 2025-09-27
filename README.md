# 🗣️ Generative AI Voice Assistant (Multilingual Speech-to-Speech)

A lightweight, pluggable voice assistant that captures spoken input, transcribes it to text (STT), generates intelligent responses using a generative AI model, and synthesizes spoken output (TTS). Designed for multilingual support with dynamic language detection, this scaffold lets you swap providers for STT, TTS, and LLMs without rewiring the core app—perfect for building custom assistants for global users.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Generative_Model-green?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Whisper](https://img.shields.io/badge/Whisper-STT_Model-blue?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/research/whisper)
[![gTTS](https://img.shields.io/badge/gTTS-TTS_Engine-orange?style=for-the-badge&logo=google&logoColor=white)](https://pypi.org/project/gTTS/)

✨ **Features**

🎙️ **Voice Input (STT)**: Real-time microphone capture and transcription with pluggable providers (e.g., Whisper, Google Speech-to-Text).

🤖 **Intelligent Responses**: Generate context-aware replies using LLMs like OpenAI, Nebius, or local models.

🔊 **Voice Output (TTS)**: Synthesize responses to natural-sounding speech with multilingual voices (e.g., gTTS, pyttsx3).

🌍 **Multilingual Support**: Auto-detect input language, respond in matching or specified languages, and handle translations seamlessly.

🧩 **Modular Design**: Swap providers in `src/` without touching app logic; supports push-to-talk or voice activity detection (VAD).

📂 **Research & Experimentation**: Dedicated folder for notes, prototypes, and model fine-tuning.

🗂️ **Project structure**
```
.
├─ src/                           # Core modules (STT/TTS/LLM helpers, utils) — extend here
├─ research/                      # Experiments, notes, scratchpads
├─ app.py                         # Main entry point (run this)
├─ requirements.txt               # Python dependencies
├─ setup.py                       # Package metadata (editable install)
├─ templete.py                    # Starter/template script (note the spelling)
├─ speech.mp3                     # Example/output audio file
└─ Multi_Lingual_assistant.egg-info/  # Packaging metadata (multilingual name)
```

🚀 **Quickstart**

**Prerequisites**
- Python 3.8 or higher
- Microphone and speakers for input/output
- Optional: API keys for cloud STT/TTS/LLM providers (e.g., OpenAI, Nebius)

**1) Environment setup**
```bash
git clone https://github.com/AbdullahRasheed45/Generative_AI-VoiceAssistant.git
cd Generative_AI-VoiceAssistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .            # Optional: Install as editable package for development
```

**2) Configuration**
```bash
# Create environment file
cat > .env << EOF
# STT Configuration
STT_PROVIDER=whisper
STT_LANG=en

# TTS Configuration
TTS_PROVIDER=gtts
TTS_LANG=en
TTS_VOICE=default

# LLM Configuration
MODEL_PROVIDER=openai
MODEL_ID=gpt-4o-mini
OPENAI_API_KEY=your_openai_key_here
NEBIUS_API_KEY=your_nebius_key_here  # Alternative provider

# Application Settings
SAMPLE_RATE=16000
VAD_ENABLED=true
LOG_LEVEL=INFO
EOF
```

**3) Run the application**
```bash
# Start the voice assistant
python app.py

# Speak a query when prompted (or press key to record)
# Listen to the synthesized response (plays via speakers and saves to speech.mp3)
```

🧠 **System architecture**

**1. Voice Input Layer (STT)**
```python
# src/stt.py - Pluggable transcription
import pyaudio  # For microphone capture

class STTProvider:
    """Handle speech-to-text with dynamic providers"""
    
    def __init__(self, provider: str = "whisper"):
        self.provider = self._load_provider(provider)
        
    def transcribe(self, audio_data: bytes) -> str:
        """Capture and transcribe audio"""
        if self.provider == "whisper":
            import whisper
            model = whisper.load_model("base")
            result = model.transcribe(audio_data)
            return result["text"]
        # Add Google/Vosk handlers as needed
```

**2. Response Generation Layer (LLM)**
```python
# src/llm.py - Generative model integration
class LLMProvider:
    """Generate responses with pluggable models"""
    
    def __init__(self, provider: str = "openai"):
        self.client = self._init_client(provider)
    
    def generate_response(self, transcript: str, language: str) -> str:
        """Call LLM for contextual reply"""
        prompt = f"Respond to: '{transcript}' in {language}. Be helpful and concise."
        if self.client == "openai":
            from openai import OpenAI
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
```

**3. Voice Output Layer (TTS)**
```python
# src/tts.py - Text-to-speech synthesis
from gtts import gTTS
import playsound

class TTSProvider:
    """Synthesize and play speech"""
    
    def __init__(self, provider: str = "gtts"):
        self.provider = provider
    
    def synthesize(self, text: str, lang: str) -> None:
        """Generate and play audio"""
        tts = gTTS(text=text, lang=lang)
        tts.save("speech.mp3")
        playsound.playsound("speech.mp3")
        # Add pyttsx3/edge-tts support
```

**4. Multilingual Detection and Handling**
```python
# src/utils.py - Language utilities
def detect_language(audio_data: bytes) -> str:
    """Auto-detect input language"""
    # Use whisper for detection or external lib
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_data, language=None)
    return result["language"]  # e.g., 'en', 'es'
```

⚙️ **Configuration and customization**

**Provider Configuration**:
```python
# src/config.py - Centralize settings
PROVIDERS = {
    'stt': {
        'whisper': {'model': 'base', 'lang': 'auto'},
        'google': {'api_key': 'required'}
    },
    'tts': {
        'gtts': {'voice': 'default'},
        'pyttsx3': {'rate': 150}
    },
    'llm': {
        'openai': {'model': 'gpt-4o-mini'},
        'nebius': {'model': 'deepseek-v3'}
    }
}
```

**Behavior Customization**:
```python
# Configurable modes
MODES = {
    'push_to_talk': "Press Enter to record",
    'vad': "Continuous listening with voice activity detection",
    'wake_word': "Listen for 'hey assistant' to activate"
}

# Audio params
AUDIO_CONFIG = {
    'sample_rate': 16000,
    'channels': 1,
    'format': pyaudio.paInt16
}
```

🗣️ **Natural language query examples**

**Basic Interactions**:
- *"What’s the weather in London today? Answer in Spanish."*
- *"Tell me a two-sentence joke."*

**Multilingual Queries**:
- *"Translate this to French: Have a great day!"*
- *"Summarize: I have a meeting at 3 PM about the new product launch…" (in detected language)*

**Command-Based**:
- *"Open my calendar."*
- *"Set a reminder for tomorrow at 10 AM."*

🔧 **Advanced features and extensions**

**Conversation Memory**:
```python
# src/memory.py - Retain context
class ConversationMemory:
    """Store and inject history"""
    
    def __init__(self, max_turns: int = 5):
        self.history = []
        
    def add_turn(self, user: str, assistant: str):
        self.history.append({"user": user, "assistant": assistant})
        if len(self.history) > self.max_turns:
            self.history.pop(0)
    
    def get_context(self) -> str:
        return "\n".join([f"User: {turn['user']}\nAssistant: {turn['assistant']}" for turn in self.history])
```

**Tool Integration**:
```python
# src/tools.py - Action handlers
class ToolHandler:
    """Execute voice commands"""
    
    def handle_tool(self, intent: str, params: Dict):
        if intent == "open_website":
            import webbrowser
            webbrowser.open(params["url"])
        elif intent == "check_time":
            from datetime import datetime
            return datetime.now().strftime("%H:%M")
```

**Streaming Support**:
```python
# src/streaming.py - Incremental processing
class StreamingAssistant:
    """Partial transcription and TTS"""
    
    def stream_response(self, partial_transcript: str):
        # Generate incremental reply
        partial_reply = self.llm.generate(partial_transcript, stream=True)
        for chunk in partial_reply:
            self.tts.synthesize_chunk(chunk)
```

🧪 **Development and testing framework**

**Template Script (templete.py)**:
```python
# templete.py - Provider testing
def test_stt_tts():
    """Quick loop for provider validation"""
    audio = record_audio(duration=5)
    text = stt.transcribe(audio)
    print(f"Transcribed: {text}")
    tts.synthesize(text, lang="en")
    print("Playing response...")

test_stt_tts()
```

**Performance Monitoring**:
```python
# src/monitor.py - Track latencies
class AssistantMonitor:
    """Log session metrics"""
    
    def log_session(self, stt_time: float, llm_time: float, tts_time: float):
        self.metrics.histogram('stt_latency', stt_time)
        self.metrics.histogram('llm_latency', llm_time)
        self.metrics.histogram('tts_latency', tts_time)
```

🔒 **Production considerations**

**Privacy and Security**:
```python
# src/privacy.py - Data handling
class PrivacyManager:
    """Anonymize and consent checks"""
    
    def check_consent(self):
        if not os.path.exists("consent.txt"):
            raise PrivacyError("User consent required for audio processing")
        
    def scrub_pii(self, text: str) -> str:
        """Remove sensitive info"""
        # Use regex/NER to mask emails, names, etc.
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
```

**Scalability and Docker**:
```bash
# Dockerfile example
FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# Run with audio access
docker run --rm --env-file .env -v /dev/snd:/dev/snd --privileged voice-assistant
```

🐛 **Troubleshooting guide**

**Common Configuration Issues**:
- **Mic/Speaker Errors** → Grant OS permissions; select correct device in config.
- **Provider Auth Fails** → Verify API keys in .env; test with local models.
- **No Audio Output** → Check speech.mp3 generation; ensure playsound/gTTS installed.

**Performance and Response Issues**:
- **High Latency** → Switch to smaller models or enable VAD for shorter clips.
- **Language Mismatch** → Force STT_LANG/TTS_LANG in .env for testing.
- **Unicode Errors** → Sanitize filenames; use UTF-8 encoding.

**Development and Debugging**:
- **Import Errors** → Activate venv and reinstall dependencies.
- **Research Folder** → Use for isolated experiments without affecting app.py.
- **Egg-Info Issues** → Regenerate with `python setup.py develop`.

📚 **Learning resources and roadmap**

**Technical Concepts Covered**:
- **Audio Processing**: Microphone capture and playback.
- **Speech AI**: STT/TTS integration with multilingual support.
- **Generative AI**: LLM prompting for conversational responses.
- **Modularity**: Provider abstraction for easy swaps.

**Future Enhancement Ideas**:
- **Wake Word Detection**: Hands-free activation.
- **Tool Extensions**: Integrate calendars, weather APIs.
- **Fine-Tuning**: Custom models in research/ for domain-specific tasks.
- **Mobile Integration**: Adapt for Android/iOS apps.

📜 **License**

MIT License - see [LICENSE](LICENSE) file for complete terms.

## 📞 Connect & Support

<div align="center">

### 🚀 Ready to Build Multilingual Voice AI?

[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://techvibes360.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdullahrasheed-/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:abdullahrasheed45@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AbdullahRasheed45)

**Let's make voice interactions smarter and more inclusive!**

</div>

---

*Built with ❤️ for developers interested in voice AI and multilingual apps. Perfect for learning STT/TTS, generative models, and modular assistant design.*
