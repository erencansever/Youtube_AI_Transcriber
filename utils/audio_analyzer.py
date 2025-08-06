"""
Audio Analysis and Emotion Detection Module
Ses analizi ve duygu tespiti için AI modülü
"""

import os
import logging
import numpy as np
import librosa
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class EmotionResult:
    """Duygu analizi sonucu"""
    emotion: str
    confidence: float
    timestamp: float

@dataclass
class ToneAnalysis:
    """Ton analizi sonucu"""
    pitch_mean: float
    pitch_std: float
    energy_mean: float
    energy_std: float
    speaking_rate: float  # kelime/dakika
    pause_frequency: float

@dataclass
class AudioAnalysis:
    """Ses analizi sonucu"""
    emotions: List[EmotionResult]
    tone: ToneAnalysis
    speech_patterns: Dict[str, float]
    overall_mood: str
    confidence_score: float

class AudioAnalyzer:
    """Ses analizi ve duygu tespiti sınıfı"""
    
    def __init__(self):
        self.emotion_labels = ['happy', 'sad', 'angry', 'neutral', 'excited', 'calm']
        self.sample_rate = 22050
        self.hop_length = 512
        
    def analyze_audio(self, audio_path: str) -> AudioAnalysis:
        """
        Ses dosyasını analiz et
        
        Args:
            audio_path: Ses dosyasının yolu
            
        Returns:
            AudioAnalysis: Analiz sonuçları
        """
        try:
            logger.info(f"🎵 Ses analizi başlatılıyor: {audio_path}")
            
            # Ses dosyasını yükle
            y, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Analizleri yap
            emotions = self._detect_emotions(y, sr)
            tone = self._analyze_tone(y, sr)
            speech_patterns = self._analyze_speech_patterns(y, sr)
            overall_mood = self._determine_overall_mood(emotions)
            confidence_score = self._calculate_confidence(emotions)
            
            result = AudioAnalysis(
                emotions=emotions,
                tone=tone,
                speech_patterns=speech_patterns,
                overall_mood=overall_mood,
                confidence_score=confidence_score
            )
            
            logger.info(f"✅ Ses analizi tamamlandı!")
            logger.info(f"🎭 Genel ruh hali: {overall_mood}")
            logger.info(f"📊 Güven skoru: {confidence_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Ses analizi hatası: {e}")
            raise Exception(f"Ses analizi başarısız: {e}")
    
    def _detect_emotions(self, y: np.ndarray, sr: int) -> List[EmotionResult]:
        """Duygu tespiti yap"""
        emotions = []
        
        # Ses dosyasını segmentlere böl (5 saniyelik)
        segment_length = 5 * sr
        num_segments = len(y) // segment_length
        
        for i in range(num_segments):
            start = i * segment_length
            end = start + segment_length
            segment = y[start:end]
            
            # Duygu analizi için özellikler çıkar
            features = self._extract_emotion_features(segment, sr)
            
            # Basit duygu sınıflandırma (gerçek projede ML modeli kullanılır)
            emotion, confidence = self._classify_emotion(features)
            
            emotions.append(EmotionResult(
                emotion=emotion,
                confidence=confidence,
                timestamp=i * 5.0
            ))
        
        return emotions
    
    def _extract_emotion_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Duygu analizi için özellikler çıkar"""
        features = {}
        
        # 1. Pitch (perde) analizi
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > 0.1]
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
        
        # 2. Enerji analizi
        rms = librosa.feature.rms(y=y)[0]
        features['energy_mean'] = np.mean(rms)
        features['energy_std'] = np.std(rms)
        
        # 3. Spektral özellikler
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        
        # 4. MFCC özellikleri
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs)
        features['mfcc_std'] = np.std(mfccs)
        
        # 5. Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features['zcr_mean'] = np.mean(zcr)
        
        return features
    
    def _classify_emotion(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Özellikleri kullanarak duygu sınıflandır"""
        # Basit kural tabanlı sınıflandırma
        # Gerçek projede ML modeli kullanılır
        
        pitch_mean = features.get('pitch_mean', 0)
        energy_mean = features.get('energy_mean', 0)
        spectral_centroid = features.get('spectral_centroid_mean', 0)
        
        # Duygu kuralları
        if energy_mean > 0.1 and pitch_mean > 200:
            return 'excited', 0.8
        elif energy_mean > 0.08 and spectral_centroid > 2000:
            return 'happy', 0.7
        elif energy_mean < 0.05 and pitch_mean < 150:
            return 'sad', 0.6
        elif energy_mean > 0.12 and spectral_centroid > 3000:
            return 'angry', 0.7
        elif energy_mean < 0.03:
            return 'calm', 0.8
        else:
            return 'neutral', 0.5
    
    def _analyze_tone(self, y: np.ndarray, sr: int) -> ToneAnalysis:
        """Ton analizi yap"""
        # Pitch analizi
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > 0.1]
        
        pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0
        pitch_std = np.std(pitch_values) if len(pitch_values) > 0 else 0
        
        # Enerji analizi
        rms = librosa.feature.rms(y=y)[0]
        energy_mean = np.mean(rms)
        energy_std = np.std(rms)
        
        # Konuşma hızı (basit hesaplama)
        # Gerçek projede daha gelişmiş algoritma kullanılır
        speaking_rate = self._estimate_speaking_rate(y, sr)
        
        # Durak sıklığı
        pause_frequency = self._calculate_pause_frequency(y, sr)
        
        return ToneAnalysis(
            pitch_mean=pitch_mean,
            pitch_std=pitch_std,
            energy_mean=energy_mean,
            energy_std=energy_std,
            speaking_rate=speaking_rate,
            pause_frequency=pause_frequency
        )
    
    def _estimate_speaking_rate(self, y: np.ndarray, sr: int) -> float:
        """Konuşma hızını tahmin et"""
        # Basit hesaplama - gerçek projede daha gelişmiş
        duration = len(y) / sr
        estimated_words = duration * 2.5  # Ortalama 2.5 kelime/saniye
        return estimated_words / (duration / 60)  # kelime/dakika
    
    def _calculate_pause_frequency(self, y: np.ndarray, sr: int) -> float:
        """Durak sıklığını hesapla"""
        # Enerji eşiği altındaki bölümleri bul
        rms = librosa.feature.rms(y=y)[0]
        threshold = np.mean(rms) * 0.3
        pauses = np.sum(rms < threshold)
        return pauses / len(rms)
    
    def _analyze_speech_patterns(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Konuşma kalıplarını analiz et"""
        patterns = {}
        
        # 1. Konuşma süresi
        patterns['speech_duration'] = len(y) / sr
        
        # 2. Ses seviyesi değişkenliği
        rms = librosa.feature.rms(y=y)[0]
        patterns['volume_variability'] = np.std(rms)
        
        # 3. Perde değişkenliği
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > 0.1]
        patterns['pitch_variability'] = np.std(pitch_values) if len(pitch_values) > 0 else 0
        
        # 4. Ritim analizi
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        patterns['speech_rhythm'] = tempo
        
        return patterns
    
    def _determine_overall_mood(self, emotions: List[EmotionResult]) -> str:
        """Genel ruh halini belirle"""
        if not emotions:
            return 'neutral'
        
        # En sık görülen duyguyu bul
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion.emotion] = emotion_counts.get(emotion.emotion, 0) + 1
        
        most_common = max(emotion_counts.items(), key=lambda x: x[1])
        return most_common[0]
    
    def _calculate_confidence(self, emotions: List[EmotionResult]) -> float:
        """Güven skorunu hesapla"""
        if not emotions:
            return 0.0
        
        avg_confidence = np.mean([e.confidence for e in emotions])
        return avg_confidence
    
    def generate_emotion_report(self, analysis: AudioAnalysis, output_path: str) -> str:
        """Duygu analizi raporu oluştur"""
        try:
            report_path = Path(output_path)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Rapor verilerini hazırla
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'overall_mood': analysis.overall_mood,
                'confidence_score': analysis.confidence_score,
                'tone_analysis': {
                    'pitch_mean': analysis.tone.pitch_mean,
                    'pitch_std': analysis.tone.pitch_std,
                    'energy_mean': analysis.tone.energy_mean,
                    'speaking_rate': analysis.tone.speaking_rate,
                    'pause_frequency': analysis.tone.pause_frequency
                },
                'speech_patterns': analysis.speech_patterns,
                'emotions_timeline': [
                    {
                        'timestamp': e.timestamp,
                        'emotion': e.emotion,
                        'confidence': e.confidence
                    }
                    for e in analysis.emotions
                ]
            }
            
            # JSON raporu kaydet
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📊 Duygu analizi raporu kaydedildi: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"❌ Rapor oluşturma hatası: {e}")
            raise
    
    def create_emotion_visualization(self, analysis: AudioAnalysis, output_path: str) -> str:
        """Duygu analizi görselleştirmesi oluştur"""
        try:
            # Görselleştirme ayarları
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('🎭 Audio Emotion Analysis Report', fontsize=16, fontweight='bold')
            
            # 1. Duygu zaman çizelgesi
            timestamps = [e.timestamp for e in analysis.emotions]
            emotions = [e.emotion for e in analysis.emotions]
            confidences = [e.confidence for e in analysis.emotions]
            
            axes[0, 0].scatter(timestamps, confidences, c=[hash(e) % 10 for e in emotions], 
                             cmap='tab10', alpha=0.7, s=50)
            axes[0, 0].set_title('Emotion Timeline')
            axes[0, 0].set_xlabel('Time (seconds)')
            axes[0, 0].set_ylabel('Confidence')
            
            # 2. Duygu dağılımı
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            axes[0, 1].pie(emotion_counts.values(), labels=emotion_counts.keys(), autopct='%1.1f%%')
            axes[0, 1].set_title('Emotion Distribution')
            
            # 3. Ton analizi
            tone_data = ['Pitch Mean', 'Energy Mean', 'Speaking Rate', 'Pause Freq']
            tone_values = [
                analysis.tone.pitch_mean,
                analysis.tone.energy_mean,
                analysis.tone.speaking_rate,
                analysis.tone.pause_frequency * 100
            ]
            
            axes[1, 0].bar(tone_data, tone_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
            axes[1, 0].set_title('Tone Analysis')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # 4. Güven skoru
            axes[1, 1].text(0.5, 0.5, f'Overall Confidence\n{analysis.confidence_score:.2f}', 
                           ha='center', va='center', fontsize=20, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
            axes[1, 1].set_title('Confidence Score')
            axes[1, 1].set_xlim(0, 1)
            axes[1, 1].set_ylim(0, 1)
            
            plt.tight_layout()
            
            # Görselleştirmeyi kaydet
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"📈 Duygu analizi görselleştirmesi kaydedildi: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Görselleştirme hatası: {e}")
            raise

# Global analyzer instance
_analyzer = None

def analyze_audio_emotions(audio_path: str, output_dir: str = "outputs/analysis") -> Dict[str, str]:
    """
    Ses dosyasının duygu analizini yap (kolay kullanım için)
    
    Args:
        audio_path: Ses dosyasının yolu
        output_dir: Çıktı klasörü
    
    Returns:
        Dict: Analiz sonuçları (rapor ve görselleştirme dosyaları)
    """
    global _analyzer
    
    if _analyzer is None:
        _analyzer = AudioAnalyzer()
    
    # Analiz yap
    analysis = _analyzer.analyze_audio(audio_path)
    
    # Çıktı dosyalarını oluştur
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"{output_dir}/emotion_report_{timestamp}.json"
    viz_path = f"{output_dir}/emotion_analysis_{timestamp}.png"
    
    # Rapor ve görselleştirme oluştur
    report_file = _analyzer.generate_emotion_report(analysis, report_path)
    viz_file = _analyzer.create_emotion_visualization(analysis, viz_path)
    
    return {
        'analysis': analysis,
        'report_file': report_file,
        'visualization_file': viz_file
    } 