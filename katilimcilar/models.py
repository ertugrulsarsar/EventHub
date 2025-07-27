# =============================================================================
# KATILIMCILAR UYGULAMASI - VERİTABANI MODELLERİ
# =============================================================================
# Bu dosya katılımcı yönetimi için gerekli veritabanı tablolarını tanımlar

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Katilimci(models.Model):
    """
    Katılımcı modeli
    
    Bu model etkinliklere katılan kişilerin bilgilerini saklar
    Her katılımcı bir kullanıcı hesabına bağlıdır
    """
    
    # Kullanıcı hesabı ile bağlantı
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
        help_text="Katılımcının kullanıcı hesabı"
    )
    
    # Kişisel bilgiler
    telefon = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Telefon numarası geçerli formatta olmalıdır. Örnek: +905551234567"
            )
        ],
        verbose_name="Telefon",
        help_text="İletişim telefon numarası"
    )
    
    dogum_tarihi = models.DateField(
        null=True,
        blank=True,
        verbose_name="Doğum Tarihi",
        help_text="Katılımcının doğum tarihi"
    )
    
    # Adres bilgileri
    adres = models.TextField(
        blank=True,
        verbose_name="Adres",
        help_text="Katılımcının adres bilgisi"
    )
    
    sehir = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Şehir",
        help_text="Yaşadığı şehir"
    )
    
    # Profil bilgileri
    bio = models.TextField(
        blank=True,
        verbose_name="Hakkında",
        help_text="Katılımcı hakkında kısa bilgi"
    )
    
    profil_resmi = models.ImageField(
        upload_to='profil_resimleri/',
        null=True,
        blank=True,
        verbose_name="Profil Resmi",
        help_text="Profil fotoğrafı"
    )
    
    # Sosyal medya linkleri
    website = models.URLField(
        blank=True,
        verbose_name="Website",
        help_text="Kişisel website adresi"
    )
    
    linkedin = models.URLField(
        blank=True,
        verbose_name="LinkedIn",
        help_text="LinkedIn profil linki"
    )
    
    twitter = models.URLField(
        blank=True,
        verbose_name="Twitter",
        help_text="Twitter profil linki"
    )
    
    # Tercihler
    email_bildirim = models.BooleanField(
        default=True,
        verbose_name="E-posta Bildirimleri",
        help_text="E-posta ile bildirim almak istiyor mu?"
    )
    
    sms_bildirim = models.BooleanField(
        default=False,
        verbose_name="SMS Bildirimleri",
        help_text="SMS ile bildirim almak istiyor mu?"
    )
    
    # Sistem bilgileri
    kayit_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Kayıt Tarihi"
    )
    
    son_guncelleme = models.DateTimeField(
        auto_now=True,
        verbose_name="Son Güncelleme"
    )
    
    def __str__(self):
        """
        Admin panelinde görünecek metin
        """
        return f"{self.user.get_full_name() or self.user.username}"
    
    @property
    def yas(self):
        """
        Katılımcının yaşını hesaplar
        """
        if self.dogum_tarihi:
            from datetime import date
            bugun = date.today()
            return bugun.year - self.dogum_tarihi.year - (
                (bugun.month, bugun.day) < (self.dogum_tarihi.month, self.dogum_tarihi.day)
            )
        return None
    
    @property
    def tam_ad(self):
        """
        Katılımcının tam adını döndürür
        """
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        """
        Katılımcının e-posta adresini döndürür
        """
        return self.user.email
    
    def katildigi_etkinlik_sayisi(self):
        """
        Katıldığı etkinlik sayısını döndürür
        """
        # Bu metod kayıtlar uygulaması oluşturulduktan sonra güncellenecek
        return 0
    
    def aktif_katilim_sayisi(self):
        """
        Aktif katılım sayısını döndürür
        """
        # Bu metod kayıtlar uygulaması oluşturulduktan sonra güncellenecek
        return 0
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Katılımcı"
        verbose_name_plural = "Katılımcılar"
        ordering = ['user__first_name', 'user__last_name']


class KatilimciGrubu(models.Model):
    """
    Katılımcı grupları modeli
    
    Bu model katılımcıları gruplara ayırmak için kullanılır
    Örnek: Öğrenciler, Çalışanlar, VIP Katılımcılar
    """
    
    # Grup bilgileri
    ad = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Grup Adı",
        help_text="Grubun adı"
    )
    
    aciklama = models.TextField(
        blank=True,
        verbose_name="Açıklama",
        help_text="Grup hakkında açıklama"
    )
    
    # Grup ayarları
    renk = models.CharField(
        max_length=7,
        default="#007bff",
        verbose_name="Renk",
        help_text="Grubun temsil rengi (hex kodu)"
    )
    
    icon = models.CharField(
        max_length=50,
        default="people",
        verbose_name="İkon",
        help_text="Bootstrap icon adı"
    )
    
    # Grup üyeleri
    katilimcilar = models.ManyToManyField(
        Katilimci,
        blank=True,
        verbose_name="Katılımcılar",
        help_text="Bu gruba ait katılımcılar"
    )
    
    # Sistem bilgileri
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma Tarihi"
    )
    
    def __str__(self):
        """
        Admin panelinde görünecek metin
        """
        return self.ad
    
    @property
    def uye_sayisi(self):
        """
        Gruptaki üye sayısını döndürür
        """
        return self.katilimcilar.count()
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Katılımcı Grubu"
        verbose_name_plural = "Katılımcı Grupları"
        ordering = ['ad'] 