# =============================================================================
# ETKİNLİKLER UYGULAMASI - ADMIN PANELİ
# =============================================================================
# Bu dosya Django admin panelinde etkinliklerin nasıl görüneceğini belirler
# Admin paneli, veritabanı yönetimi için kullanıcı dostu bir arayüz sağlar

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Kategori, Etkinlik


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """
    Kategori modeli için admin paneli yapılandırması
    
    Bu sınıf, admin panelinde kategorilerin nasıl görüneceğini ve
    hangi işlemlerin yapılabileceğini belirler
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'ad',                    # Kategori adı
        'icon',                  # İkon adı
        'etkinlik_sayisi',       # Bu kategorideki etkinlik sayısı
        'olusturma_tarihi'       # Oluşturulma tarihi
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
            'fields': ('icon',)
        }),
        ('Sistem Bilgileri', {
            'fields': ('olusturma_tarihi',),
            'classes': ('collapse',)  # Gizlenebilir bölüm
        }),
    )
    
    def etkinlik_sayisi(self, obj):
        """
        Bu kategorideki etkinlik sayısını döndürür
        
        Bu metod, admin panelinde her kategori için
        o kategorideki etkinlik sayısını gösterir
        """
        count = obj.etkinlik_set.count()
        return f"{count} etkinlik"
    
    # Sütun başlığını Türkçe yap
    etkinlik_sayisi.short_description = "Etkinlik Sayısı"


@admin.register(Etkinlik)
class EtkinlikAdmin(admin.ModelAdmin):
    """
    Etkinlik modeli için admin paneli yapılandırması
    
    Bu sınıf, admin panelinde etkinliklerin nasıl görüneceğini ve
    hangi işlemlerin yapılabileceğini belirler
    """
    
    # Admin panelinde görünecek alanlar
    list_display = [
        'baslik',                # Etkinlik başlığı
        'kategori',              # Kategori
        'organizator',           # Organizatör
        'durum',                 # Durum (düzenlenebilir)
        'durum_badge',           # Durum (renkli badge)
        'baslangic_tarihi',      # Başlangıç tarihi
        'kapasite_bilgisi',      # Kapasite bilgisi
        'doluluk_orani_bar'      # Doluluk oranı (progress bar)
    ]
    
    # Arama yapılabilecek alanlar
    search_fields = [
        'baslik', 
        'aciklama', 
        'yer', 
        'organizator__username',
        'organizator__first_name',
        'organizator__last_name'
    ]
    
    # Filtreleme seçenekleri
    list_filter = [
        'kategori',
        'durum',
        'baslangic_tarihi',
        'organizator',
        'ucret'
    ]
    
    # Tarih hiyerarşisi (tarihe göre gruplama)
    date_hierarchy = 'baslangic_tarihi'
    
    # Sadece okuma modunda olan alanlar
    readonly_fields = [
        'olusturma_tarihi', 
        'guncelleme_tarihi',
        'mevcut_katilimci'
    ]
    
    # Düzenleme formunda görünecek alanlar (gruplandırılmış)
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('baslik', 'aciklama', 'kategori', 'resim')
        }),
        ('Tarih ve Saat', {
            'fields': ('baslangic_tarihi', 'bitis_tarihi')
        }),
        ('Yer Bilgileri', {
            'fields': ('yer', 'adres')
        }),
        ('Kapasite ve Durum', {
            'fields': ('maksimum_katilimci', 'mevcut_katilimci', 'durum')
        }),
        ('Organizatör ve Ücret', {
            'fields': ('organizator', 'ucret')
        }),
        ('Sistem Bilgileri', {
            'fields': ('olusturma_tarihi', 'guncelleme_tarihi'),
            'classes': ('collapse',)  # Gizlenebilir bölüm
        }),
    )
    
    # Admin panelinde gösterilecek öğe sayısı
    list_per_page = 20
    
    # Hızlı düzenleme için alanlar
    list_editable = ['durum']
    
    def durum_badge(self, obj):
        """
        Durumu renkli badge olarak gösterir
        
        Bu metod, etkinliğin durumunu Bootstrap badge'i olarak gösterir
        """
        renk_map = {
            'planlandi': 'secondary',
            'aktif': 'success',
            'tamamlandi': 'info',
            'iptal': 'danger'
        }
        
        durum_text = dict(Etkinlik.DURUM_CHOICES)[obj.durum]
        renk = renk_map.get(obj.durum, 'secondary')
        
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            renk,
            durum_text
        )
    
    def kapasite_bilgisi(self, obj):
        """
        Kapasite bilgisini gösterir
        
        Bu metod, mevcut ve maksimum katılımcı sayısını gösterir
        """
        return f"{obj.mevcut_katilimci} / {obj.maksimum_katilimci}"
    
    def doluluk_orani_bar(self, obj):
        """
        Doluluk oranını progress bar olarak gösterir
        
        Bu metod, etkinliğin doluluk oranını görsel bir bar olarak gösterir
        """
        oran = obj.doluluk_orani
        
        # Doluluk oranına göre renk belirle
        if oran >= 90:
            renk = 'danger'  # Kırmızı (neredeyse dolu)
        elif oran >= 70:
            renk = 'warning'  # Sarı (dolu)
        else:
            renk = 'success'  # Yeşil (boş)
        
        return format_html(
            '<div class="progress" style="width: 100px;">'
            '<div class="progress-bar bg-{}" role="progressbar" '
            'style="width: {}%" aria-valuenow="{}" '
            'aria-valuemin="0" aria-valuemax="100">'
            '{}%</div></div>',
            renk, oran, oran, oran
        )
    
    # Sütun başlıklarını Türkçe yap
    durum_badge.short_description = "Durum"
    kapasite_bilgisi.short_description = "Kapasite"
    doluluk_orani_bar.short_description = "Doluluk"
    
    # CSS stilleri ekle (admin panelinde görsel iyileştirmeler için)
    class Media:
        css = {
            'all': ('admin/css/etkinlik_admin.css',)
        }


# Admin paneli başlığını özelleştir
admin.site.site_header = "Etkinlik Yönetimi - Admin Paneli"
admin.site.site_title = "Etkinlik Yönetimi"
admin.site.index_title = "Hoş Geldiniz - Etkinlik Yönetimi Sistemine" 