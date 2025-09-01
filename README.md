# 🎯 EventHub - Etkinlik Yönetimi Sistemi

Modern etkinlik yönetimi sistemi. Django + FastAPI hibrit yapısı ile geliştirilmiş.

## ✨ Özellikler

- 🎪 **Etkinlik Yönetimi** - Oluşturma, düzenleme, kategori sistemi
- 👥 **Kullanıcı Sistemi** - Katılımcı ve organizatör rolleri  
- 📝 **Kayıt Sistemi** - Etkinlik kayıtları ve durum takibi
- 🔧 **Modern Tech Stack** - Django + FastAPI + Tailwind CSS
- 📱 **Responsive Design** - Mobil uyumlu arayüz
- 🌐 **REST API** - FastAPI ile modern API

## 🚀 Hızlı Başlangıç

```bash
# 1. Projeyi klonla
git clone https://github.com/ertugrulsarsar/EventHub.git
cd EventHub

# 2. Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Environment ayarla
copy env.example .env  # Windows
# cp env.example .env    # Linux/Mac

# Yeni migration
python manage.py makemigrations

# 5. Veritabanını oluştur
python manage.py migrate
python manage.py create_sample_data

# Admin kullanıcı oluştur
python manage.py createsuperuser

# 6. Sunucuları başlat
python manage.py runserver          # Terminal 1 - Django (Port 8000)
python main.py                      # Terminal 2 - FastAPI (Port 8001)
```

## 🌐 Erişim

- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin  
- **API Docs**: http://localhost:8001/docs

## 🛠️ Tech Stack

- **Backend**: Django 5.x, FastAPI
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Frontend**: Tailwind CSS, JavaScript
- **API**: FastAPI + SQLAlchemy


## 🔧 Geliştirme

```bash
# Test çalıştır
python manage.py test

# Yeni migration
python manage.py makemigrations

# Admin kullanıcı oluştur
python manage.py createsuperuser
```

## 📊 API Endpoints

- `GET /api/v1/etkinlikler/` - Etkinlik listesi
- `POST /api/v1/etkinlikler/` - Yeni etkinlik
- `GET /api/v1/kayitlar/` - Kayıt listesi
- `GET /api/v1/stats` - İstatistikler


⭐ **Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!**