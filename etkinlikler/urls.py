# =============================================================================
# ETKİNLİKLER UYGULAMASI - URL YAPILANDIRMASI
# =============================================================================
# Bu dosya etkinlikler uygulamasının URL'lerini tanımlar
# Her URL, belirli bir view fonksiyonuna yönlendirilir

from django.urls import path
from . import views

# Uygulama adı (namespace için)
app_name = 'etkinlikler'

# URL pattern'leri
urlpatterns = [
    # Ana sayfa - Tüm etkinliklerin listesi
    # URL: /
    path('', views.etkinlik_listesi, name='etkinlik_listesi'),
    
    # Etkinlik detay sayfası
    # URL: /etkinlik/1/ (1 = etkinlik ID'si)
    path('etkinlik/<int:etkinlik_id>/', views.etkinlik_detay, name='etkinlik_detay'),
    
    # Yeni etkinlik oluşturma
    # URL: /yeni/
    path('yeni/', views.etkinlik_olustur, name='etkinlik_olustur'),
    
    # Etkinlik düzenleme
    # URL: /etkinlik/1/duzenle/ (1 = etkinlik ID'si)
    path('etkinlik/<int:etkinlik_id>/duzenle/', views.etkinlik_duzenle, name='etkinlik_duzenle'),
    
    # Etkinlik silme
    # URL: /etkinlik/1/sil/ (1 = etkinlik ID'si)
    path('etkinlik/<int:etkinlik_id>/sil/', views.etkinlik_sil, name='etkinlik_sil'),
    
    # Kategori bazında etkinlik listesi
    # URL: /kategori/seminer/ (seminer = kategori adı)
    path('kategori/<str:kategori_adi>/', views.kategori_etkinlikleri, name='kategori_etkinlikleri'),
    
    # Etkinlik arama
    # URL: /ara/?q=python (q = arama terimi)
    path('ara/', views.etkinlik_ara, name='etkinlik_ara'),
    
    # Yaklaşan etkinlikler
    # URL: /yaklasan/
    path('yaklasan/', views.yaklasan_etkinlikler, name='yaklasan_etkinlikler'),
    
    # Geçmiş etkinlikler
    # URL: /gecmis/
    path('gecmis/', views.gecmis_etkinlikler, name='gecmis_etkinlikler'),
    
    # Organizatörün etkinlikleri
    # URL: /organizator/ahmet/ (ahmet = kullanıcı adı)
    path('organizator/<str:username>/', views.organizator_etkinlikleri, name='organizator_etkinlikleri'),
    
    # Yakındaki etkinlikler
    # URL: /yakindaki/?lat=41.0082&lng=28.9784&radius=10
    path('yakindaki/', views.yakindaki_etkinlikler, name='yakindaki_etkinlikler'),
    
    # Eventbrite ile ilgili url'ler kaldırıldı
] 