# =============================================================================
# KAYITLAR UYGULAMASI - ADMIN PANELİ
# =============================================================================
# Bu dosya Django admin panelinde kayıtların nasıl görüneceğini belirler

from django.contrib import admin
from django.utils.html import format_html
from .models import Kayit, KayitGecmisi


@admin.register(Kayit)
class KayitAdmin(admin.ModelAdmin):
    """
    Kayıt modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'katilimci',
        'etkinlik',
        'durum_badge',
        'kayit_turu_badge',
        'odendi',
        'kayit_tarihi'
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = [
        'katilimci__username',
        'katilimci__first_name',
        'katilimci__last_name',
        'etkinlik__baslik',
        'notlar'
    ]
    
    # Filtreleme seçenekleri
    list_filter = [
        'durum',
        'kayit_turu',
        'odendi',
        'kayit_tarihi',
        'etkinlik__kategori'
    ]
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = ['kayit_tarihi', 'guncelleme_tarihi']
    
    # Düzenleme formunda görünecek alanlar
    fieldsets = (
        ('Kayıt Bilgileri', {
            'fields': ('katilimci', 'etkinlik')
        }),
        ('Durum ve Tür', {
            'fields': ('durum', 'kayit_turu')
        }),
        ('Ödeme Bilgileri', {
            'fields': ('odendi', 'odeme_tarihi', 'odeme_yontemi')
        }),
        ('Ek Bilgiler', {
            'fields': ('notlar',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('kayit_tarihi', 'guncelleme_tarihi'),
            'classes': ('collapse',)
        }),
    )
    
    def durum_badge(self, obj):
        """
        Durumu renkli badge olarak gösterir
        """
        renk_map = {
            'beklemede': 'warning',
            'onaylandi': 'success',
            'reddedildi': 'danger',
            'iptal_edildi': 'secondary',
            'tamamlandi': 'info'
        }
        
        durum_text = dict(Kayit.DURUM_CHOICES)[obj.durum]
        renk = renk_map.get(obj.durum, 'secondary')
        
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            renk,
            durum_text
        )
    
    def kayit_turu_badge(self, obj):
        """
        Kayıt türünü renkli badge olarak gösterir
        """
        renk_map = {
            'normal': 'primary',
            'vip': 'warning',
            'erken_kayit': 'success',
            'indirimli': 'info'
        }
        
        tur_text = dict(Kayit.KAYIT_TURU_CHOICES)[obj.kayit_turu]
        renk = renk_map.get(obj.kayit_turu, 'primary')
        
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            renk,
            tur_text
        )
    
    # Sütun başlıklarını Türkçe yap
    durum_badge.short_description = "Durum"
    kayit_turu_badge.short_description = "Kayıt Türü"


@admin.register(KayitGecmisi)
class KayitGecmisiAdmin(admin.ModelAdmin):
    """
    Kayıt geçmişi modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'kayit',
        'eski_durum',
        'yeni_durum',
        'degistiren',
        'degisiklik_tarihi'
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = [
        'kayit__katilimci__username',
        'kayit__etkinlik__baslik',
        'degistiren__username',
        'notlar'
    ]
    
    # Filtreleme seçenekleri
    list_filter = [
        'eski_durum',
        'yeni_durum',
        'degisiklik_tarihi'
    ]
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = ['degisiklik_tarihi']
    
    # Düzenleme formunda görünecek alanlar
    fieldsets = (
        ('Kayıt Bilgisi', {
            'fields': ('kayit',)
        }),
        ('Değişiklik Bilgileri', {
            'fields': ('eski_durum', 'yeni_durum')
        }),
        ('Değişiklik Yapan', {
            'fields': ('degistiren',)
        }),
        ('Notlar', {
            'fields': ('notlar',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('degisiklik_tarihi',),
            'classes': ('collapse',)
        }),
    ) 