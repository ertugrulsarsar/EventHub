# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - VERİTABANI MODELLERİ
# =============================================================================
# Bu dosya organizatör yönetimi için gerekli veritabanı tablolarını tanımlar

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Organizator(models.Model):
    """
    Organizatör modeli
    
    Bu model etkinlik organize eden kişilerin bilgilerini saklar
    Her organizatör bir kullanıcı hesabına bağlıdır
    """
    
    # Kullanıcı hesabı ile bağlantı
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
        help_text="Organizatörün kullanıcı hesabı"
    )
    
    # Organizatör bilgileri
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
    
    # Organizasyon bilgileri
    organizasyon_adi = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Organizasyon Adı",
        help_text="Çalıştığı organizasyonun adı"
    )
    
    pozisyon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Pozisyon",
        help_text="Organizasyondaki pozisyonu"
    )
    
    # İletişim bilgileri
    website = models.URLField(
        blank=True,
        verbose_name="Website",
        help_text="Organizasyon website adresi"
    )
    
    adres = models.TextField(
        blank=True,
        verbose_name="Adres",
        help_text="Organizasyon adresi"
    )
    
    # Profil bilgileri
    bio = models.TextField(
        blank=True,
        verbose_name="Hakkında",
        help_text="Organizatör hakkında kısa bilgi"
    )
    
    profil_resmi = models.ImageField(
        upload_to='organizator_resimleri/',
        null=True,
        blank=True,
        verbose_name="Profil Resmi",
        help_text="Profil fotoğrafı"
    )
    
    # Sosyal medya
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
    
    # Yetkilendirme
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Doğrulanmış",
        help_text="Organizatör hesabı doğrulanmış mı?"
    )
    
    is_premium = models.BooleanField(
        default=False,
        verbose_name="Premium",
        help_text="Premium organizatör mü?"
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
    def tam_ad(self):
        """
        Organizatörün tam adını döndürür
        """
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        """
        Organizatörün e-posta adresini döndürür
        """
        return self.user.email
    
    def etkinlik_sayisi(self):
        """
        Organizatörün etkinlik sayısını döndürür
        """
        from etkinlikler.models import Etkinlik
        return Etkinlik.objects.filter(organizator=self.user).count()
    
    def aktif_etkinlik_sayisi(self):
        """
        Organizatörün aktif etkinlik sayısını döndürür
        """
        from etkinlikler.models import Etkinlik
        return Etkinlik.objects.filter(
            organizator=self.user,
            durum__in=['planlandi', 'aktif']
        ).count()
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Organizatör"
        verbose_name_plural = "Organizatörler"
        ordering = ['user__first_name', 'user__last_name']


class OrganizatorGrubu(models.Model):
    """
    Organizatör grupları modeli
    
    Bu model organizatörleri gruplara ayırmak için kullanılır
    Örnek: Kurumsal Organizatörler, Bireysel Organizatörler
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
        default="#28a745",
        verbose_name="Renk",
        help_text="Grubun temsil rengi (hex kodu)"
    )
    
    icon = models.CharField(
        max_length=50,
        default="people-fill",
        verbose_name="İkon",
        help_text="Bootstrap icon adı"
    )
    
    # Grup üyeleri
    organizatorler = models.ManyToManyField(
        Organizator,
        blank=True,
        verbose_name="Organizatörler",
        help_text="Bu gruba ait organizatörler"
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
        return self.organizatorler.count()
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Organizatör Grubu"
        verbose_name_plural = "Organizatör Grupları"
        ordering = ['ad'] 