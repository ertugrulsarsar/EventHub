# =============================================================================
# ETKİNLİKLER UYGULAMASI - CONTEXT PROCESSORS
# =============================================================================
# Bu dosya tüm template'lerde kullanılabilir context verilerini tanımlar

from .models import Kategori


def kategoriler(request):
    """
    Tüm template'lerde kategorileri kullanılabilir yapar
    
    Bu context processor:
    - Tüm kategorileri getirir
    - Base template'de dropdown menüler için kullanılır
    """
    return {
        'kategoriler': Kategori.objects.all().order_by('ad')
    } 