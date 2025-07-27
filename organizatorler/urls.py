# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - URL YAPILANDIRMASI
# =============================================================================
# Bu dosya organizatörler uygulamasının URL'lerini tanımlar

from django.urls import path
from . import views

# Uygulama adı (namespace için)
app_name = 'organizatorler'

# URL pattern'leri
urlpatterns = [
    # Authentication
    # URL: /organizatorler/login/
    path('login/', views.login_view, name='login'),
    
    # URL: /organizatorler/logout/
    path('logout/', views.logout_view, name='logout'),
    
    # Organizatör profili
    # URL: /organizatorler/profil/
    path('profil/', views.profil, name='profil'),
    
    # Organizatörün etkinlikleri
    # URL: /organizatorler/etkinliklerim/
    path('etkinliklerim/', views.etkinliklerim, name='etkinliklerim'),
    
    # Kayıt sayfası
    # URL: /organizatorler/kayit/
    path('kayit/', views.kayit, name='kayit'),
    
    # Profil düzenleme
    # URL: /organizatorler/profil/duzenle/
    path('profil/duzenle/', views.profil_duzenle, name='profil_duzenle'),
] 