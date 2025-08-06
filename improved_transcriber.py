#!/usr/bin/env python3
"""
YouTube Video Audio Downloader and Transcriber
Gelişmiş versiyon - hata yönetimi, loglama ve daha iyi kullanıcı deneyimi ile
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
except ImportError as e:
    print(f"❌ Gerekli modüller bulunamadı: {e}")
    print("📦 Lütfen gerekli paketleri yükleyin: pip install -r requirements.txt")
    sys.exit(1)

# Konfigürasyon
class Config:
    OUTPUT_PATH = Path("outputs/transcripts")
    LOG_PATH = Path("logs")
    SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a']
    MAX_RETRIES = 3
    
    @classmethod
    def setup_directories(cls):
        """Gerekli klasörleri oluştur"""
        cls.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
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

def main():
    """Ana program akışı"""
    print("🎬 YouTube Video Transkripsiyon Aracı")
    print("=" * 40)
    
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
        
        # Sonucu kaydet
        filename = get_safe_filename(url)
        if save_transcript(transcript, filename):
            print(f"\n🎉 İşlem başarıyla tamamlandı!")
            print(f"📁 Dosya konumu: {Config.OUTPUT_PATH / f'{filename}.txt'}")
            print(f"📝 Karakter sayısı: {len(transcript):,}")
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