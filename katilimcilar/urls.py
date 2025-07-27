# =============================================================================
# KATILIMCILAR UYGULAMASI - URL YAPILANDIRMASI
# =============================================================================
# Bu dosya katılımcılar uygulamasının URL'lerini tanımlar

from django.urls import path
from . import views

# Uygulama adı (namespace için)
app_name = 'katilimcilar'

# URL pattern'leri
urlpatterns = [
    # Katılımcı kayıt
    # URL: /katilimcilar/kayit/
    path('kayit/', views.kayit, name='kayit'),
    
    # Katılımcı listesi
    # URL: /katilimcilar/
    path('', views.katilimci_listesi, name='katilimci_listesi'),
    
    # Katılımcı detayı
    # URL: /katilimcilar/1/ (1 = katılımcı ID'si)
    path('<int:katilimci_id>/', views.katilimci_detay, name='katilimci_detay'),
    
    # Katılımcı profili (giriş yapmış kullanıcı için)
    # URL: /katilimcilar/profil/
    path('profil/', views.profil, name='profil'),
    
    # Profil düzenleme
    # URL: /katilimcilar/profil/duzenle/
    path('profil/duzenle/', views.profil_duzenle, name='profil_duzenle'),
] 