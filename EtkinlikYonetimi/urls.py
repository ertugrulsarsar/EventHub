# =============================================================================
# ETKİNLİK YÖNETİMİ - ANA URL YAPILANDIRMASI
# =============================================================================
# Bu dosya tüm URL'lerin nasıl yönlendirileceğini belirler
# Her URL, belirli bir view fonksiyonuna yönlendirilir

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL pattern'leri tanımla
urlpatterns = [
    # Django admin paneli
    # http://localhost:8000/admin/ adresinden erişilir
    path('admin/', admin.site.urls),
    
    # Ana sayfa ve etkinlik yönetimi
    # http://localhost:8000/ adresinden erişilir
    path('', include('etkinlikler.urls')),
    
    # Katılımcı yönetimi
    # http://localhost:8000/katilimcilar/ adresinden erişilir
    path('katilimcilar/', include('katilimcilar.urls')),
    
    # Kayıt sistemi
    # http://localhost:8000/kayitlar/ adresinden erişilir
    path('kayitlar/', include('kayitlar.urls')),
    
    # Organizatör yönetimi ve kimlik doğrulama
    # http://localhost:8000/organizatorler/ adresinden erişilir
    path('organizatorler/', include('organizatorler.urls')),
]

# Geliştirme ortamında medya dosyalarını sunmak için
# Production'da web sunucusu (nginx, apache) kullanılmalı
if settings.DEBUG:
    # Medya dosyaları için URL pattern'leri ekle
    # Bu, kullanıcıların yüklediği resimlerin görüntülenmesini sağlar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Statik dosyalar için URL pattern'leri ekle
    # Bu, CSS, JS dosyalarının sunulmasını sağlar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 