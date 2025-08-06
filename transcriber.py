"""
Audio Transcription Module using OpenAI Whisper
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import whisper
from tqdm import tqdm

logger = logging.getLogger(__name__)

class AudioTranscriber:
    """Ses dosyalarını metne çeviren sınıf"""
    
    def __init__(self, model_name: str = "base", language: Optional[str] = None):
        """
        Transkripsiyon sınıfını başlat
        
        Args:
            model_name: Whisper model adı (tiny, base, small, medium, large)
            language: Dil kodu (tr, en, fr, de, vb.) - None ise otomatik algılama
        """
        self.model_name = model_name
        self.language = language
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Whisper modelini yükle"""
        try:
            logger.info(f"🤖 Whisper modeli yükleniyor: {self.model_name}")
            self.model = whisper.load_model(self.model_name)
            logger.info(f"✅ Model başarıyla yüklendi: {self.model_name}")
        except Exception as e:
            logger.error(f"❌ Model yükleme hatası: {e}")
            raise Exception(f"Whisper modeli yüklenemedi: {e}")
    
    def transcribe(self, audio_path: str, **kwargs) -> str:
        """
        Ses dosyasını metne çevir
        
        Args:
            audio_path: Ses dosyasının yolu
            **kwargs: Ek parametreler (task, language, verbose, vb.)
        
        Returns:
            str: Transkripsiyon metni
        """
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Ses dosyası bulunamadı: {audio_path}")
        
        # Varsayılan parametreler
        default_options = {
            'task': 'transcribe',
            'verbose': False,
            'fp16': False,  # CPU kullanımı için False
        }
        
        # Dil belirtilmişse ekle
        if self.language:
            default_options['language'] = self.language
        
        # Kullanıcı parametrelerini birleştir
        options = {**default_options, **kwargs}
        
        try:
            logger.info(f"🎙️ Transkripsiyon başlatılıyor: {audio_path}")
            
            # Dosya boyutunu kontrol et
            file_size = os.path.getsize(audio_path)
            logger.info(f"📊 Ses dosyası boyutu: {file_size:,} byte")
            
            # Transkripsiyon işlemi
            with tqdm(total=100, desc="🎙️ Transkripsiyon", unit="%") as pbar:
                # Progress callback (basit simülasyon)
                pbar.update(10)
                
                result = self.model.transcribe(audio_path, **options)
                pbar.update(90)
            
            transcript = result.get('text', '').strip()
            
            if not transcript:
                logger.warning("⚠️ Transkripsiyon sonucu boş!")
                return ""
            
            # İstatistikler
            word_count = len(transcript.split())
            char_count = len(transcript)
            
            logger.info(f"✅ Transkripsiyon tamamlandı!")
            logger.info(f"📝 Kelime sayısı: {word_count:,}")
            logger.info(f"📊 Karakter sayısı: {char_count:,}")
            
            # Dil bilgisi
            detected_language = result.get('language', 'Bilinmiyor')
            logger.info(f"🌍 Algılanan dil: {detected_language}")
            
            return transcript
            
        except Exception as e:
            logger.error(f"❌ Transkripsiyon hatası: {e}")
            raise Exception(f"Ses transkripsiyonu başarısız: {e}")
    
    def transcribe_with_timestamps(self, audio_path: str, **kwargs) -> Dict[str, Any]:
        """
        Zaman damgaları ile transkripsiyon yap
        
        Args:
            audio_path: Ses dosyasının yolu
            **kwargs: Ek parametreler
        
        Returns:
            Dict: Transkripsiyon sonucu (text, segments, vb.)
        """
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Ses dosyası bulunamadı: {audio_path}")
        
        # Varsayılan parametreler
        default_options = {
            'task': 'transcribe',
            'verbose': False,
            'fp16': False,
            'word_timestamps': True,  # Kelime bazında zaman damgaları
        }
        
        if self.language:
            default_options['language'] = self.language
        
        options = {**default_options, **kwargs}
        
        try:
            logger.info(f"🎙️ Detaylı transkripsiyon başlatılıyor: {audio_path}")
            
            result = self.model.transcribe(audio_path, **options)
            
            logger.info(f"✅ Detaylı transkripsiyon tamamlandı!")
            logger.info(f"📊 Segment sayısı: {len(result.get('segments', []))}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Detaylı transkripsiyon hatası: {e}")
            raise Exception(f"Detaylı transkripsiyon başarısız: {e}")
    
    def get_available_models(self) -> list:
        """Kullanılabilir model listesini döndür"""
        return ["tiny", "base", "small", "medium", "large"]
    
    def get_supported_languages(self) -> list:
        """Desteklenen dillerin listesini döndür"""
        return [
            "tr", "en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko", "zh",
            "ar", "hi", "nl", "pl", "sv", "da", "no", "fi", "hu", "cs", "sk",
            "sl", "hr", "bs", "sr", "bg", "mk", "sq", "el", "ro", "uk", "be",
            "et", "lv", "lt", "mt", "ga", "cy", "is", "fo", "kl", "mi", "sm",
            "to", "fj", "haw", "co", "oc", "ca", "eu", "gl", "an", "ast",
            "qu", "ay", "gn", "gu", "pa", "bn", "ta", "te", "kn", "ml", "si",
            "th", "lo", "my", "ka", "am", "ti", "om", "so", "sw", "zu", "af",
            "xh", "st", "tn", "ts", "ss", "ve", "rw", "ak", "tw", "ee", "yo",
            "ig", "ha", "ne", "ur", "fa", "ps", "ku", "sd", "he", "yi", "jv",
            "su", "id", "ms", "tl", "vi", "km", "bo", "dz", "mn", "ug", "ky",
            "kk", "uz", "tk", "az", "hy", "ka", "ab", "os", "cv", "tt", "ba",
            "sah", "alt", "xal", "krc", "ady", "kbd", "ce", "inh", "lez",
            "tab", "dar", "lbe", "rut", "agx", "tkr", "tsr", "udi", "udm",
            "myv", "mdf", "mns", "mhr", "mrj", "udm", "myv", "mdf", "mns",
            "mhr", "mrj", "udm", "myv", "mdf", "mns", "mhr", "mrj"
        ]

# Global transcriber instance
_transcriber = None

def transcribe(audio_path: str, model_name: str = "base", language: Optional[str] = None, **kwargs) -> str:
    """
    Ses dosyasını metne çevir (kolay kullanım için)
    
    Args:
        audio_path: Ses dosyasının yolu
        model_name: Whisper model adı
        language: Dil kodu
        **kwargs: Ek parametreler
    
    Returns:
        str: Transkripsiyon metni
    """
    global _transcriber
    
    # Model değişmişse yeniden yükle
    if _transcriber is None or _transcriber.model_name != model_name:
        _transcriber = AudioTranscriber(model_name=model_name, language=language)
    elif language and _transcriber.language != language:
        _transcriber.language = language
    
    return _transcriber.transcribe(audio_path, **kwargs)

def transcribe_with_timestamps(audio_path: str, model_name: str = "base", language: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """
    Zaman damgaları ile transkripsiyon yap (kolay kullanım için)
    
    Args:
        audio_path: Ses dosyasının yolu
        model_name: Whisper model adı
        language: Dil kodu
        **kwargs: Ek parametreler
    
    Returns:
        Dict: Transkripsiyon sonucu
    """
    global _transcriber
    
    if _transcriber is None or _transcriber.model_name != model_name:
        _transcriber = AudioTranscriber(model_name=model_name, language=language)
    elif language and _transcriber.language != language:
        _transcriber.language = language
    
    return _transcriber.transcribe_with_timestamps(audio_path, **kwargs)

def get_model_info(model_name: str = "base") -> Dict[str, Any]:
    """
    Model bilgilerini döndür
    
    Args:
        model_name: Model adı
    
    Returns:
        Dict: Model bilgileri
    """
    model_info = {
        "tiny": {"params": "39M", "multilingual": True, "speed": "Fastest"},
        "base": {"params": "74M", "multilingual": True, "speed": "Fast"},
        "small": {"params": "244M", "multilingual": True, "speed": "Medium"},
        "medium": {"params": "769M", "multilingual": True, "speed": "Slow"},
        "large": {"params": "1550M", "multilingual": True, "speed": "Slowest"},
    }
    
    return model_info.get(model_name, {"params": "Unknown", "multilingual": False, "speed": "Unknown"}) 