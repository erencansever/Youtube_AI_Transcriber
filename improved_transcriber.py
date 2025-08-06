#!/usr/bin/env python3
"""
YouTube Video Audio Downloader and Transcriber
Gelişmiş versiyon - hata yönetimi, loglama, duygu analizi ve daha iyi kullanıcı deneyimi ile
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional
import time
from datetime import datetime

# Kendi modüllerimizi import ediyoruz
try:
    from utils.downloader import download_audio
    from utils.transcriber import transcribe
    from utils.audio_analyzer import analyze_audio_emotions
except ImportError as e:
    print(f"❌ Gerekli modüller bulunamadı: {e}")
    print("📦 Lütfen gerekli paketleri yükleyin: pip install -r requirements.txt")
    sys.exit(1)

# Konfigürasyon
class Config:
    OUTPUT_PATH = Path("outputs/transcripts")
    ANALYSIS_PATH = Path("outputs/analysis")
    LOG_PATH = Path("logs")
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a']
    MAX_RETRIES = 3
    
    @classmethod
    def setup_directories(cls):
        """Gerekli klasörleri oluştur"""
        cls.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
        cls.ANALYSIS_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_PATH.mkdir(parents=True, exist_ok=True)

# Loglama ayarları
def setup_logging():
    """Loglama sistemini kur"""
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
    """YouTube URL'sinin geçerli olup olmadığını kontrol et"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)

def get_safe_filename(url: str) -> str:
    """URL'den güvenli dosya adı oluştur"""
    # URL'den video ID'sini çıkar (basit yöntem)
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
            logger.info(f"✅ Ses başarıyla indirildi: {audio_path}")
            return audio_path
        except Exception as e:
            logger.warning(f"❌ İndirme hatası (deneme {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 3 saniye sonra tekrar deneniyor...")
                time.sleep(3)
            else:
                logger.error(f"❌ {max_retries} deneme sonrası indirme başarısız")
                return None

def transcribe_with_retry(audio_path: str, max_retries: int = Config.MAX_RETRIES) -> Optional[str]:
    """Hata durumunda tekrar deneme ile transkripsiyon"""
    for attempt in range(max_retries):
        try:
            logger.info(f"🎙️ Transkripsiyon denemesi {attempt + 1}/{max_retries}")
            transcript = transcribe(audio_path)
            logger.info("✅ Transkripsiyon başarıyla tamamlandı")
            return transcript
        except Exception as e:
            logger.warning(f"❌ Transkripsiyon hatası (deneme {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 5 saniye sonra tekrar deneniyor...")
                time.sleep(5)
            else:
                logger.error(f"❌ {max_retries} deneme sonrası transkripsiyon başarısız")
                return None

def analyze_emotions_with_retry(audio_path: str, max_retries: int = Config.MAX_RETRIES) -> Optional[dict]:
    """Hata durumunda tekrar deneme ile duygu analizi"""
    for attempt in range(max_retries):
        try:
            logger.info(f"🎭 Duygu analizi denemesi {attempt + 1}/{max_retries}")
            analysis_results = analyze_audio_emotions(audio_path, str(Config.ANALYSIS_PATH))
            logger.info("✅ Duygu analizi başarıyla tamamlandı")
            return analysis_results
        except Exception as e:
            logger.warning(f"❌ Duygu analizi hatası (deneme {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                logger.info("🔄 3 saniye sonra tekrar deneniyor...")
                time.sleep(3)
            else:
                logger.error(f"❌ {max_retries} deneme sonrası duygu analizi başarısız")
                return None

def save_transcript(transcript: str, filename: str) -> bool:
    """Transkripti dosyaya kaydet"""
    try:
        output_file = Config.OUTPUT_PATH / f"{filename}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        logger.info(f"💾 Transkript kaydedildi: {output_file}")
        
        # Dosya boyutunu göster
        file_size = output_file.stat().st_size
        logger.info(f"📊 Dosya boyutu: {file_size:,} byte")
        
        return True
    except Exception as e:
        logger.error(f"❌ Dosya kaydetme hatası: {e}")
        return False

def cleanup_audio_file(audio_path: str) -> None:
    """Geçici ses dosyasını temizle"""
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"🧹 Geçici ses dosyası temizlendi: {audio_path}")
    except Exception as e:
        logger.warning(f"⚠️ Ses dosyası temizlenemedi: {e}")

def display_analysis_summary(analysis_results: dict) -> None:
    """Duygu analizi özetini göster"""
    if not analysis_results or 'analysis' not in analysis_results:
        return
    
    analysis = analysis_results['analysis']
    
    print("\n" + "="*50)
    print("🎭 DUYGU ANALİZİ SONUÇLARI")
    print("="*50)
    
    # Genel ruh hali
    print(f"🌍 Genel Ruh Hali: {analysis.overall_mood.upper()}")
    print(f"📊 Güven Skoru: {analysis.confidence_score:.2f}")
    
    # Ton analizi
    print(f"\n🎵 TON ANALİZİ:")
    print(f"   • Ortalama Perde: {analysis.tone.pitch_mean:.1f} Hz")
    print(f"   • Ortalama Enerji: {analysis.tone.energy_mean:.3f}")
    print(f"   • Konuşma Hızı: {analysis.tone.speaking_rate:.1f} kelime/dakika")
    print(f"   • Durak Sıklığı: {analysis.tone.pause_frequency:.2f}")
    
    # Konuşma kalıpları
    print(f"\n🗣️ KONUŞMA KALIPLARI:")
    print(f"   • Konuşma Süresi: {analysis.speech_patterns.get('speech_duration', 0):.1f} saniye")
    print(f"   • Ses Değişkenliği: {analysis.speech_patterns.get('volume_variability', 0):.3f}")
    print(f"   • Perde Değişkenliği: {analysis.speech_patterns.get('pitch_variability', 0):.1f}")
    
    # Duygu dağılımı
    emotion_counts = {}
    for emotion in analysis.emotions:
        emotion_counts[emotion.emotion] = emotion_counts.get(emotion.emotion, 0) + 1
    
    print(f"\n😊 DUYGU DAĞILIMI:")
    for emotion, count in emotion_counts.items():
        percentage = (count / len(analysis.emotions)) * 100
        print(f"   • {emotion.capitalize()}: {percentage:.1f}% ({count} segment)")
    
    # Dosya konumları
    if 'report_file' in analysis_results:
        print(f"\n📄 Rapor Dosyası: {analysis_results['report_file']}")
    if 'visualization_file' in analysis_results:
        print(f"📈 Görselleştirme: {analysis_results['visualization_file']}")

def main():
    """Ana program akışı"""
    print("🎬 YouTube Video Transkripsiyon ve Duygu Analizi Aracı")
    print("=" * 60)
    
    # Klasörleri oluştur
    Config.setup_directories()
    
    # Loglama sistemini başlat
    global logger
    logger = setup_logging()
    
    try:
        # Kullanıcıdan URL al
        while True:
            url = input("🎥 YouTube URL'sini girin (çıkmak için 'q'): ").strip()
            
            if url.lower() in ['q', 'quit', 'exit']:
                print("👋 Program sonlandırılıyor...")
                break
            
            if not url:
                print("❌ URL boş olamaz!")
                continue
            
            if not validate_youtube_url(url):
                print("❌ Geçersiz YouTube URL'si! Lütfen doğru bir YouTube linki girin.")
                continue
            
            break
        
        if url.lower() in ['q', 'quit', 'exit']:
            return
        
        # Duygu analizi yapılsın mı?
        emotion_analysis = input("🎭 Duygu analizi yapılsın mı? (y/n): ").strip().lower() in ['y', 'yes', 'evet']
        
        # Ses indirme
        logger.info("🚀 İşlem başlatılıyor...")
        audio_path = download_with_retry(url)
        
        if not audio_path:
            logger.error("❌ Ses indirme başarısız oldu. Program sonlandırılıyor.")
            return
        
        # Transkripsiyon
        logger.info("🎙️ Transkripsiyon başlatılıyor...")
        transcript = transcribe_with_retry(audio_path)
        
        if not transcript:
            logger.error("❌ Transkripsiyon başarısız oldu. Program sonlandırılıyor.")
            cleanup_audio_file(audio_path)
            return
        
        # Duygu analizi
        analysis_results = None
        if emotion_analysis:
            logger.info("🎭 Duygu analizi başlatılıyor...")
            analysis_results = analyze_emotions_with_retry(audio_path)
            
            if analysis_results:
                display_analysis_summary(analysis_results)
            else:
                logger.warning("⚠️ Duygu analizi başarısız oldu, devam ediliyor...")
        
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