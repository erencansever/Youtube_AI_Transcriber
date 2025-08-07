#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path
from typing import Optional
import time
from datetime import datetime
try:
    from utils.downloader import download_audio
    from utils.transcriber import transcribe
    from utils.audio_analyzer import analyze_audio_emotions
except ImportError as e:
    print(f" No reuired modules: {e}")
    print(" Please install the necessarry packages: pip install -r requirements.txt")
    sys.exit(1)
class Config:
    OUTPUT_PATH = Path("outputs/transcripts")
    ANALYSIS_PATH = Path("outputs/analysis")
    LOG_PATH = Path("logs")
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a']
    MAX_RETRIES = 3
    
    @classmethod
    def setup_directories(cls):
        cls.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        cls.ANALYSIS_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_PATH.mkdir(parents=True, exist_ok=True)

def setup_logging():
    log_file = Config.LOG_PATH / f"transcriber_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def validate_youtube_url(url: str) -> bool:
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)

def get_safe_filename(url: str) -> str:
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
    else:
        video_id = str(int(time.time()))
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"transcript_{video_id}_{timestamp}"

def download_with_retry(url: str, max_retries: int = Config.MAX_RETRIES) -> Optional[str]:
    """Hata durumunda tekrar deneme ile ses indirme"""
    for attempt in range(max_retries):
        try:
            logger.info(f"🎥 Ses indirme denemesi {attempt + 1}/{max_retries}")
            audio_path = download_audio(url)
            logger.info(f" Audio sucessfully installed: {audio_path}")
            return audio_path
        except Exception as e:
            logger.warning(f" Installazation mistake (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 retrying after 3 seconds...")
                time.sleep(3)
            else:
                logger.error(f" {max_retries} unsucceseful install after retry")
                return None

def transcribe_with_retry(audio_path: str, max_retries: int = Config.MAX_RETRIES) -> Optional[str]:
    for attempt in range(max_retries):
        try:
            logger.info(f"🎙️ Transcription attempt {attempt + 1}/{max_retries}")
            transcript = transcribe(audio_path)
            logger.info(" Succesfull Transcribing")
            return transcript
        except Exception as e:
            logger.warning(f" Transcribe mistake (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 retrying after 5 seconds...")
                time.sleep(5)
            else:
                logger.error(f" {max_retries} unsuccesfull transcribing after retry")
                return None

def analyze_emotions_with_retry(audio_path: str, max_retries: int = Config.MAX_RETRIES) -> Optional[dict]:
    for attempt in range(max_retries):
        try:
            logger.info(f" Emotion analysis attempt {attempt + 1}/{max_retries}")
            analysis_results = analyze_audio_emotions(audio_path, str(Config.ANALYSIS_PATH))
            logger.info(" Emotion analysis sucessfully done !!")
            return analysis_results
        except Exception as e:
            logger.warning(f" Emotion Analysis fail (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 retrying after 3 seconds...")
                time.sleep(3)
            else:
                logger.error(f" {max_retries} emotion analysis fail after retry")
                return None

def save_transcript(transcript: str, filename: str) -> bool:
    try:
        output_file = Config.OUTPUT_PATH / f"{filename}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        logger.info(f" Transcript saved at: {output_file}")
        
        # Dosya boyutunu göster
        file_size = output_file.stat().st_size
        logger.info(f" File size: {file_size:,} byte")
        
        return True
    except Exception as e:
        logger.error(f" File saving fail: {e}")
        return False

def cleanup_audio_file(audio_path: str) -> None:
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Temporary audio file cleaned: {audio_path}")
    except Exception as e:
        logger.warning(f"Audio file couldn't be cleaned: {e}")

def display_analysis_summary(analysis_results: dict) -> None:
    if not analysis_results or 'analysis' not in analysis_results:
        return
    
    analysis = analysis_results['analysis']
    
    print("\n" + "="*50)
    print("🎭 EMOTİON ANALYSIS RESULTS")
    print("="*50)
    
    print(f"🌍 General Emotion: {analysis.overall_mood.upper()}")
    print(f"📊 Confidince Score: {analysis.confidence_score:.2f}")
    
    # Ton analizi
    print(f"\n🎵 TONE ANALYSIS:")
    print(f"   • Average Pitch: {analysis.tone.pitch_mean:.1f} Hz")
    print(f"   • Average Tone Energy: {analysis.tone.energy_mean:.3f}")
    print(f"   • Speaking rate: {analysis.tone.speaking_rate:.1f} kelime/dakika")
    print(f"   • Pause Frequency: {analysis.tone.pause_frequency:.2f}")
    
    # Konuşma kalıpları
    print(f"\n🗣️ SPEECH PATTERNS:")
    print(f"   • Speech Duration: {analysis.speech_patterns.get('speech_duration', 0):.1f} saniye")
    print(f"   • Volume Variability: {analysis.speech_patterns.get('volume_variability', 0):.3f}")
    print(f"   • Pitch Variability: {analysis.speech_patterns.get('pitch_variability', 0):.1f}")
    
    # Duygu dağılımı
    emotion_counts = {}
    for emotion in analysis.emotions:
        emotion_counts[emotion.emotion] = emotion_counts.get(emotion.emotion, 0) + 1
    
    print(f"\n😊 EMOTİONS:")
    for emotion, count in emotion_counts.items():
        percentage = (count / len(analysis.emotions)) * 100
        print(f"   • {emotion.capitalize()}: {percentage:.1f}% ({count} segment)")
    
    # Dosya konumları
    if 'report_file' in analysis_results:
        print(f"\n📄 Report File: {analysis_results['report_file']}")
    if 'visualization_file' in analysis_results:
        print(f"📈 Visualization: {analysis_results['visualization_file']}")

def main():
    print("🎬 YouTube Video Transcription and Emotion Analysis Tool")
    print("=" * 60)
    
    Config.setup_directories()
    global logger
    logger = setup_logging()
    
    try:
        while True:
            url = input("🎥 Enter Youtube URL ('q' to exit): ").strip()
            
            if url.lower() in ['q', 'quit', 'exit']:
                print("Exiting...")
                break
            
            if not url:
                print("URL can not be empty.")
                continue
            
            if not validate_youtube_url(url):
                print("Invalid Youtube URL. Please enter a valid Youtube URL.")
                continue
            
            break
        
        if url.lower() in ['q', 'quit', 'exit']:
            return
        
        emotion_analysis = input("Would you like to perform Emotion Analysis (y/n): ").strip().lower() in ['y', 'yes', 'evet']
       
        logger.info("Program is starting...")
        audio_path = download_with_retry(url)
        
        if not audio_path:
            logger.error("Audio install is unsuccesful. Terminating the progress...")
            return
        
        # Transkripsiyon
        logger.info("Initializing the transcription...")
        transcript = transcribe_with_retry(audio_path)
        
        if not transcript:
            logger.error("Unsuccesfull Transcription. Terminating the progress...")
            cleanup_audio_file(audio_path)
            return
        
        # Duygu analizi
        analysis_results = None
        if emotion_analysis:
            logger.info("Initializing emotion analysis...")
            analysis_results = analyze_emotions_with_retry(audio_path)
            
            if analysis_results:
                display_analysis_summary(analysis_results)
            else:
                logger.warning("Unsucessful emotion analysis. Continuing...")
        
        # Sonucu kaydet
        filename = get_safe_filename(url)
        if save_transcript(transcript, filename):
            print(f"\n🎉 İşlem başarıyla tamamlandı!")
            print(f"📁 Transkript: {Config.OUTPUT_PATH / f'{filename}.txt'}")
            print(f"📝 Karakter sayısı: {len(transcript):,}")
            
            if analysis_results:
                print(f"🎭 Duygu analizi: {Config.ANALYSIS_PATH}")
        else:
            logger.error("❌ Dosya kaydetme başarısız!")
        
        # Temizlik
        cleanup_audio_file(audio_path)
        
    except KeyboardInterrupt:
        logger.info("⏹️ Kullanıcı tarafından durduruldu")
        print("\n⏹️ İşlem durduruldu.")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        print(f"❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    main() 
