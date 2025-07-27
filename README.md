# 🎯 EventHub - Etkinlik Yönetimi Sistemi

Modern ve kapsamlı etkinlik yönetimi sistemi. Django + FastAPI hibrit yapısı ile geliştirilmiş, kullanıcı dostu arayüzü ile etkinlik oluşturma, katılım ve yönetim işlemlerini kolaylaştıran web uygulaması.

## 📋 Özellikler

### 🎪 Etkinlik Yönetimi

- **Etkinlik Oluşturma**: Detaylı etkinlik bilgileri ile kolay oluşturma
- **Kategori Sistemi**: Etkinlikleri kategorilere ayırma (Seminer, Konser, Spor, vb.)
- **Kapasite Yönetimi**: Otomatik doluluk takibi ve progress bar'lar
- **Durum Takibi**: Planlandı, Aktif, Tamamlandı, İptal durumları
- **Resim Yükleme**: Etkinlik resimleri için destek
- **Tarih/Saat Yönetimi**: Başlangıç ve bitiş tarihleri
- **Arama ve Filtreleme**: Gelişmiş arama ve kategori bazlı filtreleme

### 👥 Katılımcı Yönetimi

- **Profil Sistemi**: Detaylı katılımcı profilleri
- **Grup Yönetimi**: Katılımcıları gruplara ayırma
- **İletişim Bilgileri**: Telefon, e-posta, adres bilgileri
- **Sosyal Medya**: LinkedIn, Twitter, website linkleri
- **Bildirim Tercihleri**: E-posta ve SMS bildirim seçenekleri

### 📝 Kayıt Sistemi

- **Kayıt Olma**: Etkinliklere kolay kayıt
- **Durum Takibi**: Beklemede, Onaylandı, Reddedildi, İptal
- **Kayıt Türleri**: Normal, VIP, Erken Kayıt, İndirimli
- **Ödeme Takibi**: Ödeme durumu ve yöntemi
- **Geçmiş Takibi**: Tüm değişikliklerin kaydı

### 🔧 Teknik Özellikler

- **Django Admin**: Güçlü admin paneli
- **FastAPI**: Modern REST API
- **Tailwind CSS**: Modern ve responsive tasarım
- **SQLite**: Geliştirme için, production'da PostgreSQL
- **Modüler Yapı**: SOLID prensiplerine uygun
- **Responsive Design**: Mobil uyumlu tasarım

## 🚀 Kurulum

### 1. Gereksinimler

```bash
# Python 3.8+ gerekli
python --version

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 3. Veritabanını Oluştur

```bash
# Django migrations
python manage.py makemigrations
python manage.py migrate

# Örnek veriler oluştur
python manage.py create_sample_data

# Süper kullanıcı oluştur
python manage.py createsuperuser
```

### 4. Sunucuları Başlat

```bash
# Django sunucusu (Terminal 1)
python manage.py runserver

# FastAPI sunucusu (Terminal 2)
uvicorn main:app --reload --port 8001
```

## 🌐 Erişim

- **Django Web**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **FastAPI**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 📁 Proje Yapısı

```
etkinlik_yonetimi/
├── EtkinlikYonetimi/          # Ana Django projesi
│   ├── settings.py            # Proje ayarları
│   ├── urls.py                # Ana URL yapılandırması
│   └── wsgi.py                # WSGI uygulaması
├── etkinlikler/               # Etkinlik yönetimi
│   ├── models.py              # Veritabanı modelleri
│   ├── views.py               # View fonksiyonları
│   ├── forms.py               # Form sınıfları
│   ├── admin.py               # Admin paneli
│   └── urls.py                # URL yapılandırması
├── katilimcilar/              # Katılımcı yönetimi
│   ├── models.py              # Katılımcı modelleri
│   ├── views.py               # Katılımcı view'ları
│   └── urls.py                # URL yapılandırması
├── kayitlar/                  # Kayıt sistemi
│   ├── models.py              # Kayıt modelleri
│   ├── views.py               # Kayıt view'ları
│   └── urls.py                # URL yapılandırması
├── organizatorler/            # Organizatör yönetimi
│   ├── models.py              # Organizatör modelleri
│   ├── views.py               # Organizatör view'ları
│   └── urls.py                # URL yapılandırması
├── api/                       # FastAPI modülleri
│   ├── database.py            # Veritabanı bağlantısı
│   ├── models.py              # SQLAlchemy modelleri
│   ├── schemas.py             # Pydantic şemaları
│   └── routers/               # API endpoint'leri
│       ├── etkinlikler.py     # Etkinlik API'leri
│       ├── katilimcilar.py    # Katılımcı API'leri
│       └── kayitlar.py        # Kayıt API'leri
├── templates/                 # HTML şablonları
│   ├── base.html              # Ana şablon
│   ├── etkinlikler/           # Etkinlik şablonları
│   ├── katilimcilar/          # Katılımcı şablonları
│   ├── kayitlar/              # Kayıt şablonları
│   └── organizatorler/        # Organizatör şablonları
├── static/                    # CSS, JS, resimler
│   ├── css/                   # Stil dosyaları
│   └── js/                    # JavaScript dosyaları
├── media/                     # Yüklenen dosyalar
│   └── etkinlik_resimleri/    # Etkinlik resimleri
├── main.py                    # FastAPI ana dosyası
├── manage.py                  # Django yönetim aracı
└── requirements.txt           # Python bağımlılıkları
```

## 🔌 API Endpoint'leri

### Etkinlikler

- `GET /api/v1/etkinlikler/` - Tüm etkinlikleri listele
- `GET /api/v1/etkinlikler/{id}/` - Etkinlik detayı
- `POST /api/v1/etkinlikler/` - Yeni etkinlik oluştur
- `PUT /api/v1/etkinlikler/{id}/` - Etkinlik güncelle
- `DELETE /api/v1/etkinlikler/{id}/` - Etkinlik sil

### Kayıtlar

- `GET /api/v1/kayitlar/` - Tüm kayıtları listele
- `GET /api/v1/kayitlar/{id}/` - Kayıt detayı
- `POST /api/v1/kayitlar/` - Yeni kayıt oluştur
- `PUT /api/v1/kayitlar/{id}/` - Kayıt güncelle

### Katılımcılar

- `GET /api/v1/katilimcilar/` - Tüm katılımcıları listele
- `GET /api/v1/katilimcilar/{id}/` - Katılımcı detayı
- `POST /api/v1/katilimcilar/` - Yeni katılımcı oluştur

## 🎨 Özelleştirme

### Yeni Kategori Ekleme

```python
# Admin panelinden veya Django shell'den
from etkinlikler.models import Kategori

kategori = Kategori.objects.create(
    ad="Teknoloji",
    aciklama="Teknoloji ile ilgili etkinlikler",
    icon="laptop"
)
```

### Özel Durum Ekleme

```python
# models.py dosyasında DURUM_CHOICES listesine ekle
DURUM_CHOICES = [
    ('planlandi', 'Planlandı'),
    ('aktif', 'Aktif'),
    ('tamamlandi', 'Tamamlandı'),
    ('iptal', 'İptal Edildi'),
    ('yeni_durum', 'Yeni Durum'),  # Yeni durum
]
```

## 🛠️ Geliştirme

### Yeni Uygulama Ekleme

```bash
python manage.py startapp yeni_uygulama
```

### Migration Oluşturma

```bash
python manage.py makemigrations
python manage.py migrate
```

### Test Çalıştırma

```bash
python manage.py test
```

### Örnek Veri Oluşturma

```bash
python manage.py create_sample_data
```

## 📊 Veritabanı Şeması

### Ana Tablolar

- **etkinlikler_etkinlik**: Etkinlik bilgileri
- **etkinlikler_kategori**: Kategori bilgileri
- **katilimcilar_katilimci**: Katılımcı profilleri
- **kayitlar_kayit**: Etkinlik kayıtları
- **organizatorler_organizator**: Organizatör profilleri
- **auth_user**: Kullanıcı hesapları

### İlişkiler

- Her etkinlik bir kategoriye ait
- Her etkinlik bir organizatöre ait
- Her kayıt bir katılımcı ve etkinliğe bağlı
- Her katılımcı bir kullanıcı hesabına bağlı
- Her organizatör bir kullanıcı hesabına bağlı

## 🔒 Güvenlik

- **CSRF Koruması**: Django form'larında aktif
- **Authentication**: Django'nun kullanıcı sistemi
- **Authorization**: View seviyesinde yetki kontrolü
- **Input Validation**: Form ve model seviyesinde doğrulama
- **SQL Injection**: ORM kullanımı ile korunma
- **XSS Koruması**: Template escaping ile korunma

## 🚀 Production Deployment

### Gereksinimler

- **Web Sunucusu**: Nginx veya Apache
- **WSGI Sunucusu**: Gunicorn
- **Veritabanı**: PostgreSQL
- **Static Files**: CDN veya web sunucusu

### Environment Variables

```bash
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com
```

## 🎯 Kullanım Senaryoları

### Organizatör İçin

1. **Kayıt Ol**: Organizatör hesabı oluştur
2. **Etkinlik Oluştur**: Detaylı bilgilerle etkinlik ekle
3. **Yönet**: Katılımcıları görüntüle ve yönet
4. **Takip Et**: Etkinlik performansını izle

### Katılımcı İçin

1. **Keşfet**: Etkinlikleri ara ve filtrele
2. **Kayıt Ol**: İstediğin etkinliğe kayıt ol
3. **Takip Et**: Kayıt durumunu kontrol et
4. **Katıl**: Etkinlik gününde katılım sağla

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Commit yapın (`git commit -am 'Yeni özellik eklendi'`)
4. Push yapın (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Geliştirici**: Ertuğrul Sarsar
- **E-posta**: [ertugrulsarsar@gmail.com]
- **GitHub**: [github.com/ertugrulsarsar]

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 