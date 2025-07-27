# =============================================================================
# ETKİNLİKLER UYGULAMASI - VERİTABANI MODELLERİ
# =============================================================================
# Bu dosya etkinlik yönetimi için gerekli veritabanı tablolarını tanımlar
# Her model, veritabanında bir tablo oluşturur

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Kategori(models.Model):
    """
    Etkinlik kategorileri modeli
    
    Bu model etkinlikleri kategorilere ayırmak için kullanılır
    Örnek: Seminer, Konser, Spor, Eğitim, vs.
    """
    
    # Kategori adı - benzersiz olmalı
    ad = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="Kategori Adı",
        help_text="Kategorinin adını girin (örn: Seminer, Konser, Spor)"
    )
    
    # Kategori açıklaması - isteğe bağlı
    aciklama = models.TextField(
        blank=True,
        verbose_name="Açıklama",
        help_text="Kategori hakkında kısa bir açıklama"
    )
    
    # Bootstrap icon adı - frontend'de kullanılacak
    icon = models.CharField(
        max_length=50, 
        default='calendar',
        verbose_name="İkon",
        help_text="Bootstrap icon adı (örn: calendar, music, sport)"
    )
    
    # Oluşturulma tarihi
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    def __str__(self):
        """
        Admin panelinde ve diğer yerlerde görünecek metin
        """
        return self.ad
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['ad']  # Ada göre sırala


class Etkinlik(models.Model):
    """
    Ana etkinlik modeli
    
    Bu model etkinliklerin tüm bilgilerini saklar
    Her etkinlik bir organizatöre ait olur ve bir kategoriye sahiptir
    """
    
    # =============================================================================
    # TEMEL BİLGİLER
    # =============================================================================
    
    # Etkinlik başlığı
    baslik = models.CharField(
        max_length=200,
        verbose_name="Etkinlik Başlığı",
        help_text="Etkinliğin başlığını girin"
    )
    
    # Etkinlik açıklaması
    aciklama = models.TextField(
        verbose_name="Açıklama",
        help_text="Etkinlik hakkında detaylı açıklama"
    )
    
    # Kategori - her etkinlik bir kategoriye ait olmalı
    kategori = models.ForeignKey(
        Kategori, 
        on_delete=models.CASCADE,
        verbose_name="Kategori",
        help_text="Etkinliğin kategorisini seçin"
    )
    
    # =============================================================================
    # TARİH VE SAAT BİLGİLERİ
    # =============================================================================
    
    # Başlangıç tarihi ve saati
    baslangic_tarihi = models.DateTimeField(
        verbose_name="Başlangıç Tarihi",
        help_text="Etkinliğin başlayacağı tarih ve saat"
    )
    
    # Bitiş tarihi ve saati
    bitis_tarihi = models.DateTimeField(
        verbose_name="Bitiş Tarihi",
        help_text="Etkinliğin biteceği tarih ve saat"
    )
    
    # =============================================================================
    # YER BİLGİLERİ
    # =============================================================================
    
    # Etkinlik yeri
    yer = models.CharField(
        max_length=200,
        verbose_name="Yer",
        help_text="Etkinliğin yapılacağı yer (örn: Konferans Salonu)"
    )
    
    # Detaylı adres
    adres = models.TextField(
        verbose_name="Adres",
        help_text="Etkinlik yerinin detaylı adresi"
    )
    
    # =============================================================================
    # KAPASİTE VE DURUM
    # =============================================================================
    
    # Maksimum katılımcı sayısı
    maksimum_katilimci = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name="Maksimum Katılımcı",
        help_text="Etkinliğe katılabilecek maksimum kişi sayısı"
    )
    
    # Mevcut katılımcı sayısı (otomatik hesaplanacak)
    mevcut_katilimci = models.PositiveIntegerField(
        default=0,
        verbose_name="Mevcut Katılımcı",
        help_text="Şu anda kayıtlı katılımcı sayısı"
    )
    
    # Etkinlik durumu
    DURUM_CHOICES = [
        ('planlandi', 'Planlandı'),
        ('aktif', 'Aktif'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    durum = models.CharField(
        max_length=20, 
        choices=DURUM_CHOICES, 
        default='planlandi',
        verbose_name="Durum",
        help_text="Etkinliğin mevcut durumu"
    )
    
    # =============================================================================
    # ORGANİZATÖR BİLGİSİ
    # =============================================================================
    
    # Etkinliği oluşturan/organize eden kullanıcı
    organizator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Organizatör",
        help_text="Etkinliği organize eden kişi"
    )
    
    # =============================================================================
    # EK BİLGİLER
    # =============================================================================
    
    # Etkinlik ücreti (ücretsiz olabilir)
    ucret = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Ücret",
        help_text="Etkinlik ücreti (ücretsiz ise boş bırakın)"
    )
    
    # Etkinlik resmi
    resim = models.ImageField(
        upload_to='etkinlik_resimleri/', 
        null=True, 
        blank=True,
        verbose_name="Etkinlik Resmi",
        help_text="Etkinlik için bir resim yükleyin"
    )
    
    # =============================================================================
    # TARİH BİLGİLERİ
    # =============================================================================
    
    # Oluşturulma tarihi (otomatik)
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    # Son güncelleme tarihi (otomatik)
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True,
        verbose_name="Son Güncelleme"
    )
    
    # =============================================================================
    # API ENTEGRASYONU ALANLARI
    # =============================================================================
    
    # Konum bilgileri (Eventbrite API için)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Enlem",
        help_text="Etkinlik yerinin enlem koordinatı"
    )
    
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name="Boylam",
        help_text="Etkinlik yerinin boylam koordinatı"
    )
    
    # Dış API bilgileri
    external_id = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        verbose_name="Dış API ID",
        help_text="Eventbrite gibi dış API'lerden gelen etkinlik ID'si"
    )
    
    source = models.CharField(
        max_length=50, 
        default='internal',
        choices=[
            ('internal', 'Yerel'),
            ('eventbrite', 'Eventbrite'),
            ('ticketmaster', 'Ticketmaster'),
        ],
        verbose_name="Kaynak",
        help_text="Etkinliğin hangi kaynaktan geldiği"
    )
    
    def __str__(self):
        """
        Admin panelinde görünecek metin
        """
        return f"{self.baslik} - {self.baslangic_tarihi.strftime('%d.%m.%Y %H:%M')}"
    
    @property
    def kalan_yer(self):
        """
        Kalan katılımcı sayısını döndürür
        
        Bu property, maksimum kapasite ile mevcut katılımcı arasındaki farkı hesaplar
        """
        return max(0, self.maksimum_katilimci - self.mevcut_katilimci)
    
    @property
    def doluluk_orani(self):
        """
        Doluluk oranını yüzde olarak döndürür
        
        Bu property, etkinliğin ne kadar dolu olduğunu gösterir
        """
        if self.maksimum_katilimci > 0:
            return round((self.mevcut_katilimci / self.maksimum_katilimci) * 100, 1)
        return 0
    
    @property
    def durum_renk(self):
        """
        Duruma göre Bootstrap renk sınıfını döndürür
        
        Bu property, frontend'de durumu renkli göstermek için kullanılır
        """
        renk_map = {
            'planlandi': 'secondary',
            'aktif': 'success', 
            'tamamlandi': 'info',
            'iptal': 'danger'
        }
        return renk_map.get(self.durum, 'secondary')
    
    def katilimci_ekle(self):
        """
        Katılımcı sayısını bir artırır
        
        Bu metod, yeni bir kayıt oluşturulduğunda çağrılır
        """
        if self.mevcut_katilimci < self.maksimum_katilimci:
            self.mevcut_katilimci += 1
            self.save()
            return True
        return False
    
    def katilimci_cikar(self):
        """
        Katılımcı sayısını bir azaltır
        
        Bu metod, bir kayıt iptal edildiğinde çağrılır
        """
        if self.mevcut_katilimci > 0:
            self.mevcut_katilimci -= 1
            self.save()
            return True
        return False
    
    def etkinlik_aktif_mi(self):
        """
        Etkinliğin şu anda aktif olup olmadığını kontrol eder
        
        Bu metod, etkinliğin başlangıç ve bitiş tarihlerine göre durumunu belirler
        """
        simdi = timezone.now()
        return self.baslangic_tarihi <= simdi <= self.bitis_tarihi
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ['-baslangic_tarihi']  # Tarihe göre azalan sıralama 