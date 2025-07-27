# =============================================================================
# KAYITLAR UYGULAMASI - URL YAPILANDIRMASI
# =============================================================================
# Bu dosya kayıtlar uygulamasının URL'lerini tanımlar

from django.urls import path
from . import views

# Uygulama adı (namespace için)
app_name = 'kayitlar'

# URL pattern'leri
urlpatterns = [
    # Kayıt listesi
    # URL: /kayitlar/
    path('', views.kayit_listesi, name='kayit_listesi'),
    
    # Kayıt detayı
    # URL: /kayitlar/1/ (1 = kayıt ID'si)
    path('<int:kayit_id>/', views.kayit_detay, name='kayit_detay'),
    
    # Etkinliğe kayıt olma
    # URL: /kayitlar/etkinlik/1/kayit/ (1 = etkinlik ID'si)
    path('etkinlik/<int:etkinlik_id>/kayit/', views.etkinlik_kayit, name='etkinlik_kayit'),
    
    # Kayıt iptal etme
    # URL: /kayitlar/1/iptal/ (1 = kayıt ID'si)
    path('<int:kayit_id>/iptal/', views.kayit_iptal, name='kayit_iptal'),
    
    # Kullanıcının katılımları
    # URL: /kayitlar/katilimlarim/
    path('katilimlarim/', views.katilimlarim, name='katilimlarim'),
] 