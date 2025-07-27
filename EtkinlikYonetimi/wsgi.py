# =============================================================================
# ETKİNLİK YÖNETİMİ - WSGI YAPILANDIRMASI
# =============================================================================
# WSGI (Web Server Gateway Interface) - Web sunucusu ile Django arasındaki köprü
# Bu dosya production ortamında web sunucusunun Django'yu nasıl çalıştıracağını belirler

import os

from django.core.wsgi import get_wsgi_application

# Django ayarlarının bulunduğu modülü belirt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EtkinlikYonetimi.settings')

# WSGI uygulamasını oluştur
# Bu, web sunucusunun Django'yu çalıştırması için gerekli
application = get_wsgi_application() 