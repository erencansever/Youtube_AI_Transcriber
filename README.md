# 🎬 YouTube Video Transcription Tool

A powerful Python tool that downloads audio from YouTube videos and converts them to text using OpenAI Whisper.

## ✨ Features

### 🚀 Core Features
- **YouTube Video Download**: Reliable video downloading with yt-dlp
- **AI Transcription**: High-quality speech recognition with OpenAI Whisper
- **Multi-language Support**: Support for 100+ languages
- **Error Handling**: Automatic retry mechanism and detailed error reporting
- **Progress Tracking**: Real-time progress monitoring
- **Logging**: Detailed log records

### 🔧 Advanced Features
- **URL Validation**: Validates YouTube URLs
- **Safe Filenames**: Unique filenames with video ID and timestamp
- **Auto Cleanup**: Automatic cleanup of temporary files
- **Model Selection**: 5 different Whisper models (tiny, base, small, medium, large)
- **Timestamps**: Optional word-level timestamps
- **Statistics**: Detailed process statistics

## 📋 Requirements

- Python 3.8+
- FFmpeg (for audio processing)
- Internet connection

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/erencansever/Youtube_AI_Transcriber.git
cd Youtube_AI_Transcriber
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
- Download from [FFmpeg official site](https://ffmpeg.org/download.html)
- Add to system PATH

## 🚀 Usage

### Basic Usage
```bash
python main.py
```

### Program Flow
1. Enter YouTube URL
2. Program automatically:
   - Extracts video information
   - Downloads audio file
   - Performs transcription
   - Saves result
   - Cleans up temporary files

### Example Output
```
🎬 YouTube Video Transcription Tool
========================================
🎥 Enter YouTube URL (or 'q' to quit): https://youtube.com/watch?v=...
🚀 Starting process...
🎥 Analyzing YouTube video: https://youtube.com/watch?v=...
📹 Video: Example Video Title
⏱️ Duration: 5:30
📥 Downloading: 100%|██████████| 15.2MB/15.2MB [00:30<00:00]
✅ Audio successfully downloaded: /tmp/example_video.mp3
🎙️ Transcription: 100%|██████████| 100/100 [02:15<00:00]
✅ Transcription completed!
📝 Word count: 1,234
📊 Character count: 5,678
🌍 Detected language: en
💾 Transcript saved: outputs/transcripts/transcript_VIDEOID_20231201_143022.txt

🎉 Process completed successfully!
📁 File location: outputs/transcripts/transcript_VIDEOID_20231201_143022.txt
📝 Character count: 5,678
```

## 📁 File Structure

```
youtube-transcriber/
├── improved_transcriber.py    # Main program
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── utils/                    # Helper modules
│   ├── __init__.py
│   ├── downloader.py         # YouTube download module
│   └── transcriber.py        # Transcription module
├── outputs/                  # Output files
│   └── transcripts/          # Transcript files
└── logs/                     # Log files
```

## ⚙️ Configuration

### Whisper Models
- **tiny**: 39M parameters - Fastest, low accuracy
- **base**: 74M parameters - Fast, medium accuracy (default)
- **small**: 244M parameters - Medium speed, good accuracy
- **medium**: 769M parameters - Slow, high accuracy
- **large**: 1550M parameters - Slowest, highest accuracy

### Supported Languages
English, Turkish, German, French, Spanish and 100+ languages

## 🔧 Advanced Usage

### Programmatic Usage
```python
from utils.downloader import download_audio
from utils.transcriber import transcribe

# Download audio
audio_path = download_audio("https://youtube.com/watch?v=...")

# Perform transcription
transcript = transcribe(audio_path, model_name="medium", language="en")

print(transcript)
```

### Transcription with Timestamps
```python
from utils.transcriber import transcribe_with_timestamps

result = transcribe_with_timestamps(audio_path)
for segment in result['segments']:
    print(f"{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}")
```

## 🐛 Troubleshooting

### Common Errors

**1. FFmpeg not found**
```
❌ FFmpeg not found. Please install FFmpeg.
```
**Solution:** Install FFmpeg on your system.

**2. Model loading error**
```
❌ Model loading error: CUDA out of memory
```
**Solution:** Use a smaller model (tiny, base) or use CPU.

**3. YouTube download error**
```
❌ YouTube video download failed: Video unavailable
```
**Solution:** Check video URL, is the video accessible?

### Log Files
Check log files in `logs/` folder for detailed error information.

## 📊 Performance

### System Requirements
- **RAM**: Minimum 4GB (8GB+ for large model)
- **CPU**: Modern processor (GPU optional)
- **Disk**: 1GB+ free space

### Speed Comparison
| Model | Parameters | Speed | Accuracy |
|-------|-----------|-----|----------|
| tiny  | 39M       | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| base  | 74M       | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| small | 244M      | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium| 769M      | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| large | 1550M     | ⚡ | ⭐⭐⭐⭐⭐ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloading
- [FFmpeg](https://ffmpeg.org/) - Audio processing

## 📞 Support

For issues:
1. Use GitHub Issues
2. Check log files
3. Read README again

---

**Note:** This tool is for educational purposes. Please comply with laws when downloading copyrighted content.
