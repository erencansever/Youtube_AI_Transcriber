# 🎭 YouTube AI Transcriber & Emotion Analyzer

A next-generation Python tool that not only transcribes YouTube videos using OpenAI Whisper, but also performs **advanced AI-powered emotion analysis** on the audio — giving you deep insight into the mood, tone, and energy of any video!

---

## ✨ Why This Project Stands Out

### 🚀 Key Features
- **YouTube Audio Download**: Download audio from any YouTube video or short.
- **AI Transcription**: Convert speech to text with OpenAI Whisper.
- **🌈 Emotion Analysis (Highlight!)**:  
  - Detects emotions (happy, sad, angry, neutral, excited, calm) throughout the audio.
  - Provides a timeline of emotional changes.
  - Calculates overall mood and confidence score.
  - Visualizes emotion distribution and tone with beautiful charts.
- **Speech Pattern Analysis**: Analyze pitch, energy, speaking rate, and more.
- **Comprehensive Reports**: Generates both JSON and PNG visual summaries.
- **Multi-language Support**: 100+ languages.
- **Robust Error Handling**: Automatic retries and detailed logs.

---

## 🎭 Emotion Analysis: The Star Feature

**What makes this tool unique?**  
It doesn't just transcribe — it **feels** the video!

- **Emotion Timeline**: See how the mood changes every 5 seconds.
- **Overall Mood**: Instantly know if the video is happy, sad, neutral, etc.
- **Confidence Score**: How sure is the AI about its emotion detection?
- **Tone Analysis**: Average pitch, energy, speaking rate, and pauses.
- **Visual Output**:  
  - **PNG Chart**: Colorful, easy-to-read emotion and tone visualization.
  - **JSON Report**: All raw data for further analysis.

**Example Output:**
```
==================================================
🎭 EMOTION ANALYSIS RESULTS
==================================================
🌍 Overall Mood: HAPPY
📊 Confidence Score: 0.75

🎵 TONE ANALYSIS:
   • Avg Pitch: 185.3 Hz
   • Avg Energy: 0.087
   • Speaking Rate: 145.2 words/min
   • Pause Frequency: 0.12

🗣️ SPEECH PATTERNS:
   • Duration: 325.7 sec
   • Volume Variability: 0.045
   • Pitch Variability: 23.1

😊 EMOTION DISTRIBUTION:
   • Happy: 45.2% (14 segments)
   • Neutral: 32.3% (10 segments)
   • Excited: 22.5% (7 segments)

📄 Report File: outputs/analysis/emotion_report_YYYYMMDD_HHMMSS.json
📈 Visualization: outputs/analysis/emotion_analysis_YYYYMMDD_HHMMSS.png
```

---

## 📋 Requirements

- Python 3.8+
- FFmpeg (for audio processing)
- Internet connection

---

## 🛠️ Installation

```bash
git clone https://github.com/erencansever/Youtube_AI_Transcriber.git
cd Youtube_AI_Transcriber
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
brew install ffmpeg      # (macOS) or sudo apt install ffmpeg (Linux)
```

---

## 🚀 Usage

```bash
python3 improved_transcriber.py
```

- Enter the YouTube URL when prompted.
- Choose whether to run emotion analysis (`y` for yes).
- All outputs will be saved in the `outputs/` folder.

---

## 📁 Output Files

- **Transcripts**: `outputs/transcripts/`
- **Emotion Analysis Reports**: `outputs/analysis/`
  - `.json` for raw data
  - `.png` for visual charts

---

## 🧠 How It Works

- Downloads audio from YouTube.
- Transcribes speech to text using OpenAI Whisper.
- Analyzes audio for emotion, tone, and speech patterns using AI (librosa, numpy, matplotlib).
- Generates detailed reports and visualizations.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [librosa](https://librosa.org/)
- [matplotlib](https://matplotlib.org/)

---

**Note:** This tool is for educational purposes. Please comply with laws when downloading copyrighted content.
