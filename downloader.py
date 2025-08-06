"""
YouTube Video Audio Downloader Module
"""

import os
import tempfile
import logging
from pathlib import Path
from typing import Optional
import yt_dlp
from tqdm import tqdm

logger = logging.getLogger(__name__)

class ProgressHook:
    """Download progress'ını takip etmek için hook sınıfı"""
    
    def __init__(self):
        self.pbar = None
        self.downloaded_bytes = 0
        self.total_bytes = 0
    
    def __call__(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                self.total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                if self.total_bytes:
                    self.pbar = tqdm(total=self.total_bytes, unit='B', unit_scale=True, desc="📥 İndiriliyor")
            
            if self.pbar and self.total_bytes:
                downloaded = d.get('downloaded_bytes', 0)
                self.pbar.update(downloaded - self.downloaded_bytes)
                self.downloaded_bytes = downloaded
        
        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.close()
            logger.info(f"✅ İndirme tamamlandı: {d.get('filename', 'Bilinmeyen dosya')}")

def download_audio(url: str, output_dir: Optional[str] = None) -> str:
    """
    YouTube videosundan ses dosyası indir
    
    Args:
        url: YouTube video URL'si
        output_dir: Çıktı klasörü (None ise geçici klasör kullanılır)
    
    Returns:
        str: İndirilen ses dosyasının yolu
    
    Raises:
        Exception: İndirme başarısız olursa
    """
    
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # yt-dlp konfigürasyonu
    ydl_opts = {
        'format': 'bestaudio/best',  # En iyi ses kalitesi
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [ProgressHook()],
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'ignoreerrors': False,
    }
    
    try:
        logger.info(f"🎥 YouTube video analiz ediliyor: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgilerini al
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown Video')
            duration = info.get('duration', 0)
            
            logger.info(f"📹 Video: {video_title}")
            if duration:
                logger.info(f"⏱️ Süre: {duration//60}:{duration%60:02d}")
            
            # Ses dosyasını indir
            logger.info("🎵 Ses dosyası indiriliyor...")
            ydl.download([url])
            
            # İndirilen dosyayı bul
            downloaded_files = list(output_path.glob(f"*.mp3"))
            
            if not downloaded_files:
                raise Exception("İndirilen ses dosyası bulunamadı")
            
            # En son oluşturulan dosyayı al
            audio_file = max(downloaded_files, key=lambda x: x.stat().st_mtime)
            
            logger.info(f"✅ Ses dosyası başarıyla indirildi: {audio_file}")
            return str(audio_file)
            
    except yt_dlp.DownloadError as e:
        logger.error(f"❌ YouTube indirme hatası: {e}")
        raise Exception(f"YouTube videosu indirilemedi: {e}")
    
    except Exception as e:
        logger.error(f"❌ Beklenmeyen indirme hatası: {e}")
        raise Exception(f"Ses indirme başarısız: {e}")

def get_video_info(url: str) -> dict:
    """
    YouTube video bilgilerini al (indirme yapmadan)
    
    Args:
        url: YouTube video URL'si
    
    Returns:
        dict: Video bilgileri
    """
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', 'Unknown'),
                'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
            }
    except Exception as e:
        logger.error(f" Video bilgileri alınamadı: {e}")
        return {}

def cleanup_temp_files(directory: str, pattern: str = "*.mp3") -> None:
    """
    Geçici ses dosyalarını temizle
    
    Args:
        directory: Temizlenecek klasör
        pattern: Dosya pattern'i
    """
    
    try:
        temp_path = Path(directory)
        for file_path in temp_path.glob(pattern):
            if file_path.is_file():
                file_path.unlink()
                logger.debug(f"🧹 Geçici dosya silindi: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Geçici dosya temizleme hatası: {e}") 