# =============================================================================
# ETKİNLİKLER UYGULAMASI - CONTEXT PROCESSORS
# =============================================================================
# Bu dosya tüm template'lere otomatik olarak veri ekler
# Her sayfa yüklendiğinde bu fonksiyonlar çalışır

from .models import Kategori


def kategoriler(request):
    """
    Tüm kategorileri template'lere ekler
    
    Bu context processor:
    - Her sayfada kategorileri kullanılabilir hale getirir
    - Navigation menüsünde kategori listesi gösterir
    - Filtreleme seçeneklerinde kullanılır
    """
    try:
        # Tüm kategorileri getir (ada göre sıralı)
        kategoriler = Kategori.objects.all().order_by('ad')
        return {'kategoriler': kategoriler}
    except Exception as e:
        # Hata durumunda boş liste döndür
        # Bu, veritabanı henüz oluşturulmamışsa önemli
        return {'kategoriler': []} 