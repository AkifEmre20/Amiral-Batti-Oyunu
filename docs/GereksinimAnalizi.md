# Gereksinim Analizi — Amiral Battı Oyunu

## 1. Proje Tanımı
Oyuncu ile yapay zekanın karşı karşıya geldiği, 10×10 ızgara üzerinde oynanan  
klasik Amiral Battı oyununun masaüstü uygulaması.

## 2. Paydaşlar
- **Son Kullanıcı:** Oyunu oynayan öğrenci/bireysel kullanıcı  
- **Geliştirici:** BGT132 öğrencisi

## 3. Fonksiyonel Gereksinimler

| ID | Gereksinim |
|----|-----------|
| FR-01 | Kullanıcı oyuncu adı girebilmelidir |
| FR-02 | 3 zorluk seviyesi (kolay/orta/zor) seçilebilmelidir |
| FR-03 | Oyuncu gemilerini tahtaya manuel yerleştirebilmelidir |
| FR-04 | Gemi yönü (yatay/dikey) değiştirilebilmelidir |
| FR-05 | Oyuncu her turda düşman tahtasına saldırabilmelidir |
| FR-06 | AI otomatik saldırı yapmalıdır |
| FR-07 | İsabet, ıskala ve batma durumları görsel olarak gösterilmelidir |
| FR-08 | Oyun bitişinde kazanan açıkça belirtilmelidir |
| FR-09 | Skor hesaplanmalı ve kaydedilmelidir |
| FR-10 | Yüksek skor tablosu görüntülenebilmelidir |

## 4. Fonksiyonel Olmayan Gereksinimler

| ID | Gereksinim |
|----|-----------|
| NFR-01 | Oyun 60 FPS'de akıcı çalışmalıdır |
| NFR-02 | UI modern ve okunabilir olmalıdır |
| NFR-03 | Kod en az 3 OOP sınıfı içermelidir |
| NFR-04 | Hata yönetimi (try-except) uygulanmalıdır |
| NFR-05 | Modüler klasör yapısı kullanılmalıdır |

## 5. Kullanım Senaryoları

### UC-01: Oyun Başlatma
**Aktör:** Kullanıcı  
**Akış:** Menü → İsim gir → Zorluk seç → Oyna

### UC-02: Gemi Yerleştirme
**Aktör:** Kullanıcı  
**Akış:** Sol tahtaya tıkla → R ile döndür → Tüm gemiler yerleştirilince savaş başlar

### UC-03: Saldırı
**Aktör:** Kullanıcı  
**Akış:** Sağ tahtaya tıkla → İsabet/ıskala animasyonu → AI sırası → Oyun devam eder

### UC-04: Oyun Sonu
**Aktör:** Sistem  
**Akış:** Tüm gemiler batınca → Kazanan ekranı → Skor kaydedilir → Menüye dön
