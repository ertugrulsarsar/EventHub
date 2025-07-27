#!/usr/bin/env python
"""
Django'nun komut satırı yönetim aracı.

Bu dosya Django projesini yönetmek için kullanılır.
Örnek kullanımlar:
- python manage.py runserver (sunucuyu başlat)
- python manage.py migrate (veritabanı değişikliklerini uygula)
- python manage.py createsuperuser (admin kullanıcısı oluştur)
"""

import os
import sys


def main():
    """
    Django yönetim komutlarını çalıştırmak için ana fonksiyon.
    
    Bu fonksiyon:
    1. Django ayarlarını yükler
    2. Komut satırı argümanlarını işler
    3. Django komutlarını çalıştırır
    """
    # Django ayarlarının bulunduğu modülü belirt
    # Bu, Django'nun hangi settings.py dosyasını kullanacağını söyler
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EtkinlikYonetimi.settings')
    
    try:
        # Django'nun komut satırı yönetim sistemini import et
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Django yüklenemezse hata ver
        raise ImportError(
            "Django yüklenemedi. Lütfen şunları kontrol edin:\n"
            "1. Sanal ortamınızın aktif olduğundan emin olun\n"
            "2. pip install -r requirements.txt komutunu çalıştırın\n"
            "3. Django'nun doğru yüklendiğinden emin olun"
        ) from exc
    
    # Django komutunu çalıştır
    # sys.argv komut satırı argümanlarını içerir
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Bu dosya doğrudan çalıştırıldığında main() fonksiyonunu çağır
    main() 