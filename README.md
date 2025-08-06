# 🎬 YouTube Video Transkripsiyon Aracı

YouTube videolarından ses indirip, OpenAI Whisper kullanarak metne çeviren gelişmiş bir Python aracı.

## ✨ Özellikler

### 🚀 Ana Özellikler
- **YouTube Video İndirme**: yt-dlp ile güvenilir video indirme
- **AI Transkripsiyon**: OpenAI Whisper ile yüksek kaliteli konuşma tanıma
- **Çoklu Dil Desteği**: 100+ dil desteği
- **Hata Yönetimi**: Otomatik tekrar deneme ve detaylı hata raporlama
- **Progress Tracking**: Gerçek zamanlı ilerleme takibi
- **Loglama**: Detaylı log kayıtları

### 🔧 Gelişmiş Özellikler
- **URL Doğrulama**: YouTube URL'lerinin geçerliliğini kontrol
- **Güvenli Dosya Adları**: Video ID'si ve timestamp ile benzersiz dosya adları
- **Otomatik Temizlik**: Geçici dosyaların otomatik silinmesi
- **Model Seçimi**: 5 farklı Whisper modeli (tiny, base, small, medium, large)
- **Zaman Damgaları**: İsteğe bağlı kelime bazında zaman damgaları
- **İstatistikler**: Detaylı işlem istatistikleri

## 📋 Gereksinimler

- Python 3.8+
- FFmpeg (ses işleme için)
- İnternet bağlantısı

## 🛠️ Kurulum

### 1. Depoyu Klonlayın
```bash
git clone <repository-url>
cd youtube-transcriber
```

### 2. Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. FFmpeg Kurulumu

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
- [FFmpeg resmi sitesinden](https://ffmpeg.org/download.html) indirin
- Sistem PATH'ine ekleyin

## 🚀 Kullanım

### Temel Kullanım
```bash
python improved_transcriber.py
```

### Program Akışı
1. YouTube URL'sini girin
2. Program otomatik olarak:
   - Video bilgilerini alır
   - Ses dosyasını indirir
   - Transkripsiyon yapar
   - Sonucu kaydeder
   - Geçici dosyaları temizler

### Örnek Çıktı
```
🎬 YouTube Video Transkripsiyon Aracı
========================================
🎥 YouTube URL'sini girin (çıkmak için 'q'): https://youtube.com/watch?v=...
🚀 İşlem başlatılıyor...
🎥 YouTube video analiz ediliyor: https://youtube.com/watch?v=...
📹 Video: Örnek Video Başlığı
⏱️ Süre: 5:30
📥 İndiriliyor: 100%|██████████| 15.2MB/15.2MB [00:30<00:00]
✅ Ses başarıyla indirildi: /tmp/örnek_video.mp3
🎙️ Transkripsiyon: 100%|██████████| 100/100 [02:15<00:00]
✅ Transkripsiyon tamamlandı!
📝 Kelime sayısı: 1,234
📊 Karakter sayısı: 5,678
🌍 Algılanan dil: tr
💾 Transkript kaydedildi: outputs/transcripts/transcript_VIDEOID_20231201_143022.txt

🎉 İşlem başarıyla tamamlandı!
📁 Dosya konumu: outputs/transcripts/transcript_VIDEOID_20231201_143022.txt
📝 Karakter sayısı: 5,678
```

## 📁 Dosya Yapısı

```
youtube-transcriber/
├── improved_transcriber.py    # Ana program
├── requirements.txt           # Bağımlılıklar
├── README.md                 # Bu dosya
├── utils/                    # Yardımcı modüller
│   ├── __init__.py
│   ├── downloader.py         # YouTube indirme modülü
│   └── transcriber.py        # Transkripsiyon modülü
├── outputs/                  # Çıktı dosyaları
│   └── transcripts/          # Transkript dosyaları
└── logs/                     # Log dosyaları
```

## ⚙️ Konfigürasyon

### Whisper Modelleri
- **tiny**: 39M parametre - En hızlı, düşük doğruluk
- **base**: 74M parametre - Hızlı, orta doğruluk (varsayılan)
- **small**: 244M parametre - Orta hız, iyi doğruluk
- **medium**: 769M parametre - Yavaş, yüksek doğruluk
- **large**: 1550M parametre - En yavaş, en yüksek doğruluk

### Desteklenen Diller
Türkçe, İngilizce, Almanca, Fransızca, İspanyolca ve 100+ dil

## 🔧 Gelişmiş Kullanım

### Programatik Kullanım
```python
from utils.downloader import download_audio
from utils.transcriber import transcribe

# Ses indir
audio_path = download_audio("https://youtube.com/watch?v=...")

# Transkripsiyon yap
transcript = transcribe(audio_path, model_name="medium", language="tr")

print(transcript)
```

### Zaman Damgaları ile Transkripsiyon
```python
from utils.transcriber import transcribe_with_timestamps

result = transcribe_with_timestamps(audio_path)
for segment in result['segments']:
    print(f"{segment['start']:.2f}s - {segment['end']:.2f}s: {segment['text']}")
```

## 🐛 Sorun Giderme

### Yaygın Hatalar

**1. FFmpeg bulunamadı**
```
❌ FFmpeg bulunamadı. Lütfen FFmpeg'i yükleyin.
```
**Çözüm:** FFmpeg'i sisteminize yükleyin.

**2. Model yükleme hatası**
```
❌ Model yükleme hatası: CUDA out of memory
```
**Çözüm:** Daha küçük model kullanın (tiny, base) veya CPU kullanın.

**3. YouTube indirme hatası**
```
❌ YouTube videosu indirilemedi: Video unavailable
```
**Çözüm:** Video URL'sini kontrol edin, video erişilebilir mi?

### Log Dosyaları
Detaylı hata bilgileri için `logs/` klasöründeki log dosyalarını kontrol edin.

## 📊 Performans

### Sistem Gereksinimleri
- **RAM**: En az 4GB (large model için 8GB+)
- **CPU**: Modern işlemci (GPU opsiyonel)
- **Disk**: 1GB+ boş alan

### Hız Karşılaştırması
| Model | Parametre | Hız | Doğruluk |
|-------|-----------|-----|----------|
| tiny  | 39M       | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| base  | 74M       | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| small | 244M      | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium| 769M      | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| large | 1550M     | ⚡ | ⭐⭐⭐⭐⭐ |

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- [OpenAI Whisper](https://github.com/openai/whisper) - Konuşma tanıma
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube indirme
- [FFmpeg](https://ffmpeg.org/) - Ses işleme

## 📞 Destek

Sorunlarınız için:
1. GitHub Issues kullanın
2. Log dosyalarını kontrol edin
3. README'yi tekrar okuyun

---

**Not:** Bu araç eğitim amaçlıdır. Telif hakkı olan içerikleri indirirken yasalara uygun hareket edin. 