# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - YAPILANDIRMA
# =============================================================================
# Bu dosya Django'ya bu uygulamanın nasıl çalışacağını söyler

from django.apps import AppConfig


class OrganizatorlerConfig(AppConfig):
    """
    Organizatörler uygulamasının yapılandırması
    
    Bu sınıf Django'ya:
    - Uygulamanın adını
    - Varsayılan otomatik alan türünü
    - Uygulama başlatıldığında yapılacak işlemleri söyler
    """
    
    # Uygulamanın benzersiz adı
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Uygulamanın adı (settings.py'de kullanılan ad)
    name = 'organizatorler'
    
    # Uygulamanın görünen adı (admin panelinde görünür)
    verbose_name = 'Organizatör Yönetimi'
    
    def ready(self):
        """
        Uygulama başlatıldığında çalışacak kod
        
        Bu fonksiyon Django başlatıldığında bir kez çalışır
        Genellikle sinyal kayıtları, özel komutlar için kullanılır
        """
        # Şimdilik boş bırakıyoruz
        # İleride sinyal kayıtları ekleyebiliriz
        pass 