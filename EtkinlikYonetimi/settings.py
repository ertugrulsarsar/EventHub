# =============================================================================
# ETKİNLİK YÖNETİMİ - DJANGO AYARLARI
# =============================================================================
# Bu dosya Django projesinin tüm ayarlarını içerir
# Geliştirme ortamı için optimize edilmiştir

import os
from pathlib import Path
from decouple import config, Csv

# Proje kök dizinini belirle
# Bu, manage.py dosyasının bulunduğu dizindir
BASE_DIR = Path(__file__).resolve().parent.parent

# Django güvenlik anahtarı
# ⚠️ PRODUCTION'DA BU ANAHTARI DEĞİŞTİRİN!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-etkinlik-yonetimi-2024-gelistirme-ortami')

# Hata ayıklama modu
# Geliştirme sırasında True, production'da False olmalı
DEBUG = config('DEBUG', default=True, cast=bool)

# Hangi domain'lerden erişime izin verileceği
# Geliştirme sırasında boş bırakılabilir
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# =============================================================================
# DJANGO UYGULAMALARI
# =============================================================================
# Bu bölümde projede kullanılacak tüm uygulamalar listelenir

INSTALLED_APPS = [
    # Django'nun kendi uygulamaları (varsayılan)
    'django.contrib.admin',          # Admin paneli
    'django.contrib.auth',           # Kullanıcı kimlik doğrulama
    'django.contrib.contenttypes',   # İçerik türleri
    'django.contrib.sessions',       # Oturum yönetimi
    'django.contrib.messages',       # Mesaj sistemi
    'django.contrib.staticfiles',    # Statik dosyalar (CSS, JS, resimler)
    
    # Üçüncü parti uygulamalar
    'crispy_forms',                  # Bootstrap form stilleri
    'crispy_bootstrap5',             # Bootstrap 5 desteği
    
    # Kendi uygulamalarımız
    'etkinlikler',                   # Etkinlik yönetimi
    'katilimcilar',                  # Katılımcı yönetimi
    'kayitlar',                      # Kayıt sistemi
    'organizatorler',                # Organizatör yönetimi
]

# =============================================================================
# MIDDLEWARE (ARA YAZILIM)
# =============================================================================
# Her HTTP isteğinde çalışan yazılımlar

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Güvenlik
    'django.contrib.sessions.middleware.SessionMiddleware', # Oturum yönetimi
    'django.middleware.common.CommonMiddleware',          # Genel işlemler
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF koruması
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Kimlik doğrulama
    'django.contrib.messages.middleware.MessageMiddleware',    # Mesaj sistemi
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking koruması
]

# Ana URL yapılandırması
ROOT_URLCONF = 'EtkinlikYonetimi.urls'

# =============================================================================
# ŞABLON AYARLARI
# =============================================================================
# HTML dosyalarının nasıl işleneceğini belirler

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Şablon dizini
        'APP_DIRS': True,                  # Her uygulamada templates/ klasörü ara
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'etkinlikler.context_processors.kategoriler',
            ],
        },
    },
]

# WSGI uygulaması (web sunucusu için)
WSGI_APPLICATION = 'EtkinlikYonetimi.wsgi.application'

# =============================================================================
# VERİTABANI AYARLARI
# =============================================================================
# Geliştirme için SQLite kullanıyoruz
# Production'da PostgreSQL veya MySQL kullanılabilir

DATABASES = {
    'default': {
        'ENGINE': f"django.db.backends.{config('DATABASE_ENGINE', default='sqlite3')}",
        'NAME': config('DATABASE_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}

# =============================================================================
# ŞİFRE DOĞRULAMA
# =============================================================================
# Kullanıcı şifrelerinin güvenlik kuralları

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# ULUSLARARASILAŞTIRMA
# =============================================================================
# Dil ve saat dilimi ayarları

LANGUAGE_CODE = 'tr-tr'           # Türkçe
TIME_ZONE = 'Europe/Istanbul'     # İstanbul saat dilimi
USE_I18N = True                   # Uluslararasılaştırma aktif
USE_TZ = True                     # Saat dilimi desteği aktif

# =============================================================================
# STATİK DOSYALAR
# =============================================================================
# CSS, JavaScript, resim dosyaları için

STATIC_URL = '/static/'  # URL öneki - / ile başlamalı!
STATICFILES_DIRS = [BASE_DIR / 'static']  # Statik dosya dizinleri
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Production için statik dosya toplama

# =============================================================================
# MEDYA DOSYALARI
# =============================================================================
# Kullanıcıların yüklediği dosyalar (resimler, belgeler)

MEDIA_URL = '/media/'  # URL öneki
MEDIA_ROOT = BASE_DIR / 'media'  # Dosya sistemi dizini

# =============================================================================
# DİĞER AYARLAR
# =============================================================================

# Varsayılan otomatik alan türü
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms ayarları (Bootstrap form stilleri)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Giriş/çıkış yönlendirme
LOGIN_REDIRECT_URL = 'etkinlikler:etkinlik_listesi'      # Giriş sonrası etkinlik listesi
LOGOUT_REDIRECT_URL = 'etkinlikler:etkinlik_listesi'     # Çıkış sonrası etkinlik listesi

# CORS ayarları
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000', cast=Csv())

# E-posta ayarları
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Güvenlik ayarları
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000,http://127.0.0.1:8000', cast=Csv())
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

# Logging ayarları
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': config('LOG_LEVEL', default='INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
}