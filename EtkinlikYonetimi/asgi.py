# =============================================================================
# ETKİNLİK YÖNETİMİ - ASGI YAPILANDIRMASI
# =============================================================================
# ASGI (Asynchronous Server Gateway Interface) - Modern web sunucuları için
# WebSocket ve async işlemler için kullanılır (gelecekte gerekebilir)

import os

from django.core.asgi import get_asgi_application

# Django ayarlarının bulunduğu modülü belirt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EtkinlikYonetimi.settings')

# ASGI uygulamasını oluştur
# Bu, modern web sunucularının Django'yu çalıştırması için gerekli
application = get_asgi_application() 