# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - ADMIN PANELİ
# =============================================================================
# Bu dosya Django admin panelinde organizatörlerin nasıl görüneceğini belirler

from django.contrib import admin
from django.utils.html import format_html
from .models import Organizator, OrganizatorGrubu


@admin.register(Organizator)
class OrganizatorAdmin(admin.ModelAdmin):
    """
    Organizatör modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'user',
        'organizasyon_adi',
        'pozisyon',
        'etkinlik_sayisi',
        'aktif_etkinlik_sayisi',
        'is_verified',
        'is_premium',
        'kayit_tarihi'
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'organizasyon_adi',
        'pozisyon'
    ]
    
    # Filtreleme seçenekleri
    list_filter = [
        'is_verified',
        'is_premium',
        'kayit_tarihi',
        'organizasyon_adi'
    ]
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = ['kayit_tarihi', 'son_guncelleme']
    
    # Düzenleme formunda görünecek alanlar
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user',)
        }),
        ('Organizasyon Bilgileri', {
            'fields': ('organizasyon_adi', 'pozisyon', 'website', 'adres')
        }),
        ('İletişim Bilgileri', {
            'fields': ('telefon', 'bio')
        }),
        ('Sosyal Medya', {
            'fields': ('linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Profil', {
            'fields': ('profil_resmi',)
        }),
        ('Yetkilendirme', {
            'fields': ('is_verified', 'is_premium')
        }),
        ('Sistem Bilgileri', {
            'fields': ('kayit_tarihi', 'son_guncelleme'),
            'classes': ('collapse',)
        }),
    )
    
    def etkinlik_sayisi(self, obj):
        """
        Organizatörün etkinlik sayısını döndürür
        """
        return obj.etkinlik_sayisi()
    
    def aktif_etkinlik_sayisi(self, obj):
        """
        Organizatörün aktif etkinlik sayısını döndürür
        """
        return obj.aktif_etkinlik_sayisi()
    
    # Sütun başlıklarını Türkçe yap
    etkinlik_sayisi.short_description = "Toplam Etkinlik"
    aktif_etkinlik_sayisi.short_description = "Aktif Etkinlik"


@admin.register(OrganizatorGrubu)
class OrganizatorGrubuAdmin(admin.ModelAdmin):
    """
    Organizatör grubu modeli için admin paneli yapılandırması
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'ad',
        'uye_sayisi',
        'renk_goster',
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
            'fields': ('organizatorler',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('olusturma_tarihi',),
            'classes': ('collapse',)
        }),
    )
    
    def renk_goster(self, obj):
        """
        Rengi görsel olarak gösterir
        """
        return format_html(
            '<div style="background-color: {}; width: 20px; height: 20px; border-radius: 3px;"></div>',
            obj.renk
        )
    
    # Sütun başlığını Türkçe yap
    renk_goster.short_description = "Renk" 