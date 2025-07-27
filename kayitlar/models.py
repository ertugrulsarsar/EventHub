# =============================================================================
# KAYITLAR UYGULAMASI - VERİTABANI MODELLERİ
# =============================================================================
# Bu dosya etkinlik kayıt sistemi için gerekli veritabanı tablolarını tanımlar

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Kayit(models.Model):
    """
    Etkinlik kayıt modeli
    
    Bu model katılımcıların etkinliklere kayıt olma bilgilerini saklar
    Her kayıt, bir katılımcının bir etkinliğe kayıt olduğunu gösterir
    """
    
    # Kayıt bilgileri
    katilimci = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Katılımcı",
        help_text="Kayıt olan katılımcı"
    )
    
    etkinlik = models.ForeignKey(
        'etkinlikler.Etkinlik',
        on_delete=models.CASCADE,
        verbose_name="Etkinlik",
        help_text="Kayıt olunan etkinlik"
    )
    
    # Kayıt durumu
    DURUM_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
        ('iptal_edildi', 'İptal Edildi'),
        ('tamamlandi', 'Tamamlandı'),
    ]
    
    durum = models.CharField(
        max_length=20,
        choices=DURUM_CHOICES,
        default='beklemede',
        verbose_name="Durum",
        help_text="Kayıt durumu"
    )
    
    # Kayıt türü
    KAYIT_TURU_CHOICES = [
        ('normal', 'Normal Kayıt'),
        ('vip', 'VIP Kayıt'),
        ('erken_kayit', 'Erken Kayıt'),
        ('indirimli', 'İndirimli Kayıt'),
    ]
    
    kayit_turu = models.CharField(
        max_length=20,
        choices=KAYIT_TURU_CHOICES,
        default='normal',
        verbose_name="Kayıt Türü",
        help_text="Kayıt türü"
    )
    
    # Ödeme bilgileri
    odendi = models.BooleanField(
        default=False,
        verbose_name="Ödendi",
        help_text="Kayıt ücreti ödendi mi?"
    )
    
    odeme_tarihi = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ödeme Tarihi",
        help_text="Ödeme yapılan tarih"
    )
    
    odeme_yontemi = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Ödeme Yöntemi",
        help_text="Kullanılan ödeme yöntemi"
    )
    
    # Ek bilgiler
    notlar = models.TextField(
        blank=True,
        verbose_name="Notlar",
        help_text="Kayıt hakkında ek notlar"
    )
    
    # Sistem bilgileri
    kayit_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Kayıt Tarihi"
    )
    
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncelleme Tarihi"
    )
    
    def __str__(self):
        """
        Admin panelinde görünecek metin
        """
        return f"{self.katilimci.get_full_name()} - {self.etkinlik.baslik}"
    
    def clean(self):
        """
        Kayıt verilerini doğrular
        
        Bu metod:
        - Aynı kişinin aynı etkinliğe birden fazla kayıt olmasını engeller
        - Etkinlik kapasitesini kontrol eder
        - Kayıt tarihlerini kontrol eder
        """
        # Aynı kişinin aynı etkinliğe birden fazla kayıt olmasını engelle
        if not self.pk:  # Yeni kayıt
            mevcut_kayit = Kayit.objects.filter(
                katilimci=self.katilimci,
                etkinlik=self.etkinlik
            ).exists()
            
            if mevcut_kayit:
                raise ValidationError(
                    'Bu etkinliğe zaten kayıtlısınız!'
                )
        
        # Etkinlik kapasitesini kontrol et
        if self.etkinlik:
            if self.etkinlik.mevcut_katilimci >= self.etkinlik.maksimum_katilimci:
                raise ValidationError(
                    'Bu etkinlik kapasitesi dolmuştur!'
                )
    
    def save(self, *args, **kwargs):
        """
        Kayıt kaydedilirken çalışan metod
        
        Bu metod:
        - Kayıt durumuna göre etkinlik katılımcı sayısını günceller
        - Ödeme tarihini otomatik ayarlar
        """
        # Ödeme durumunu kontrol et
        if self.odendi and not self.odeme_tarihi:
            self.odeme_tarihi = timezone.now()
        
        # Kayıt durumuna göre etkinlik katılımcı sayısını güncelle
        if not self.pk:  # Yeni kayıt
            if self.durum == 'onaylandi':
                self.etkinlik.katilimci_ekle()
        else:  # Mevcut kayıt güncelleniyor
            eski_kayit = Kayit.objects.get(pk=self.pk)
            if eski_kayit.durum != self.durum:
                if self.durum == 'onaylandi' and eski_kayit.durum != 'onaylandi':
                    self.etkinlik.katilimci_ekle()
                elif eski_kayit.durum == 'onaylandi' and self.durum != 'onaylandi':
                    self.etkinlik.katilimci_cikar()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        Kayıt silinirken çalışan metod
        
        Bu metod:
        - Onaylı kayıt silinirse etkinlik katılımcı sayısını azaltır
        """
        if self.durum == 'onaylandi':
            self.etkinlik.katilimci_cikar()
        
        super().delete(*args, **kwargs)
    
    @property
    def durum_renk(self):
        """
        Duruma göre Bootstrap renk sınıfını döndürür
        """
        renk_map = {
            'beklemede': 'warning',
            'onaylandi': 'success',
            'reddedildi': 'danger',
            'iptal_edildi': 'secondary',
            'tamamlandi': 'info'
        }
        return renk_map.get(self.durum, 'secondary')
    
    @property
    def kayit_turu_renk(self):
        """
        Kayıt türüne göre Bootstrap renk sınıfını döndürür
        """
        renk_map = {
            'normal': 'primary',
            'vip': 'gold',
            'erken_kayit': 'success',
            'indirimli': 'info'
        }
        return renk_map.get(self.kayit_turu, 'primary')
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Kayıt"
        verbose_name_plural = "Kayıtlar"
        unique_together = ('katilimci', 'etkinlik')  # Aynı kişi aynı etkinliğe birden fazla kayıt olamaz
        ordering = ['-kayit_tarihi']


class KayitGecmisi(models.Model):
    """
    Kayıt geçmişi modeli
    
    Bu model kayıt durumu değişikliklerini takip eder
    Her değişiklik bu tabloya kaydedilir
    """
    
    # Kayıt bilgisi
    kayit = models.ForeignKey(
        Kayit,
        on_delete=models.CASCADE,
        verbose_name="Kayıt",
        help_text="İlgili kayıt"
    )
    
    # Değişiklik bilgileri
    eski_durum = models.CharField(
        max_length=20,
        choices=Kayit.DURUM_CHOICES,
        verbose_name="Eski Durum",
        help_text="Önceki durum"
    )
    
    yeni_durum = models.CharField(
        max_length=20,
        choices=Kayit.DURUM_CHOICES,
        verbose_name="Yeni Durum",
        help_text="Yeni durum"
    )
    
    # Değişiklik yapan kişi
    degistiren = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Değiştiren",
        help_text="Değişikliği yapan kişi"
    )
    
    # Değişiklik notu
    notlar = models.TextField(
        blank=True,
        verbose_name="Notlar",
        help_text="Değişiklik hakkında notlar"
    )
    
    # Sistem bilgileri
    degisiklik_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Değişiklik Tarihi"
    )
    
    def __str__(self):
        """
        Admin panelinde görünecek metin
        """
        return f"{self.kayit} - {self.eski_durum} → {self.yeni_durum}"
    
    class Meta:
        """
        Model meta bilgileri
        """
        verbose_name = "Kayıt Geçmişi"
        verbose_name_plural = "Kayıt Geçmişleri"
        ordering = ['-degisiklik_tarihi'] 