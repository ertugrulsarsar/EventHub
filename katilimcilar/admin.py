# =============================================================================
# KATILIMCILAR UYGULAMASI - ADMIN PANELİ
# =============================================================================
# Bu dosya Django admin panelinde katılımcıların nasıl görüneceğini belirler

from django.contrib import admin
from .models import Katilimci, KatilimciGrubu


@admin.register(Katilimci)
class KatilimciAdmin(admin.ModelAdmin):
    """
    Katılımcı modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'user',
        'telefon',
        'yas',
        'sehir',
        'katildigi_etkinlik_sayisi',
        'aktif_katilim_sayisi',
        'kayit_tarihi'
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'telefon',
        'sehir'
    ]
    
    # Filtreleme seçenekleri
    list_filter = [
        'email_bildirim',
        'sms_bildirim',
        'kayit_tarihi',
        'sehir'
    ]
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = ['kayit_tarihi', 'son_guncelleme']
    
    # Düzenleme formunda görünecek alanlar
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user',)
        }),
        ('Kişisel Bilgiler', {
            'fields': ('telefon', 'dogum_tarihi')
        }),
        ('Adres Bilgileri', {
            'fields': ('adres', 'sehir')
        }),
        ('Profil', {
            'fields': ('bio', 'profil_resmi')
        }),
        ('Sosyal Medya', {
            'fields': ('website', 'linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Bildirim Tercihleri', {
            'fields': ('email_bildirim', 'sms_bildirim')
        }),
        ('Sistem Bilgileri', {
            'fields': ('kayit_tarihi', 'son_guncelleme'),
            'classes': ('collapse',)
        }),
    )
    
    def katildigi_etkinlik_sayisi(self, obj):
        """
        Katıldığı etkinlik sayısını döndürür
        """
        return obj.katildigi_etkinlik_sayisi()
    
    def aktif_katilim_sayisi(self, obj):
        """
        Aktif katılım sayısını döndürür
        """
        return obj.aktif_katilim_sayisi()
    
    # Sütun başlıklarını Türkçe yap
    katildigi_etkinlik_sayisi.short_description = "Katıldığı Etkinlik"
    aktif_katilim_sayisi.short_description = "Aktif Katılım"


@admin.register(KatilimciGrubu)
class KatilimciGrubuAdmin(admin.ModelAdmin):
    """
    Katılımcı grubu modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'ad',
        'uye_sayisi',
        'olusturma_tarihi'
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = ['ad', 'aciklama']
    
    # Filtreleme seçenekleri
    list_filter = ['olusturma_tarihi']
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = ['olusturma_tarihi']
    
    # Düzenleme formunda görünecek alanlar
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('ad', 'aciklama')
        }),
        ('Görünüm', {
            'fields': ('renk', 'icon')
        }),
        ('Üyeler', {
            'fields': ('katilimcilar',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('olusturma_tarihi',),
            'classes': ('collapse',)
        }),
    ) 