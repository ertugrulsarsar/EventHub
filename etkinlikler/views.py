# =============================================================================
# ETKİNLİKLER UYGULAMASI - VIEW FONKSİYONLARI
# =============================================================================
# Bu dosya HTTP isteklerini işleyen view fonksiyonlarını içerir
# Her view, bir URL'den gelen isteği işler ve uygun yanıtı döndürür

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from functools import wraps
from .models import Etkinlik, Kategori
from .forms import EtkinlikForm
# Eventbrite ile ilgili importlar kaldırıldı


def organizator_required(view_func):
    """
    Organizatör yetkisi gerektiren decorator
    
    Bu decorator:
    - Kullanıcının giriş yapmış olmasını kontrol eder
    - Kullanıcının organizatör olup olmadığını kontrol eder
    - Organizatör değilse hata mesajı gösterir ve yönlendirir
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Bu işlem için giriş yapmanız gerekiyor!')
            return redirect('organizatorler:login')
        
        # Kullanıcının organizatör olup olmadığını kontrol et
        if not hasattr(request.user, 'organizator'):
            messages.error(request, 'Bu işlem için organizatör yetkisi gerekiyor!')
            return redirect('etkinlikler:etkinlik_listesi')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def etkinlik_listesi(request):
    """
    Ana sayfa - Tüm etkinliklerin listesi
    
    Bu view:
    - Tüm etkinlikleri getirir
    - Sayfalama yapar
    - Filtreleme seçenekleri sunar
    - Arama yapabilir
    """
    
    # URL parametrelerinden filtreleme seçeneklerini al
    kategori_id = request.GET.get('kategori')
    durum = request.GET.get('durum')
    arama = request.GET.get('q')
    
    # Etkinlikleri getir (varsayılan olarak en yeni önce)
    etkinlikler = Etkinlik.objects.all()
    
    # Kategori filtresi
    if kategori_id:
        etkinlikler = etkinlikler.filter(kategori_id=kategori_id)
    
    # Durum filtresi
    if durum:
        etkinlikler = etkinlikler.filter(durum=durum)
    
    # Arama filtresi
    if arama:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=arama) |
            Q(aciklama__icontains=arama) |
            Q(yer__icontains=arama) |
            Q(kategori__ad__icontains=arama)
        )
    
    # Sayfalama (her sayfada 12 etkinlik)
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    # Kategorileri getir (filtreleme için)
    kategoriler = Kategori.objects.all()
    
    # Context verilerini hazırla
    context = {
        'etkinlikler': sayfa,
        'kategoriler': kategoriler,
        'secilen_kategori': kategori_id,
        'secilen_durum': durum,
        'arama_terimi': arama,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/etkinlik_listesi.html', context)


def etkinlik_detay(request, etkinlik_id):
    """
    Etkinlik detay sayfası
    
    Bu view:
    - Belirli bir etkinliğin detaylarını gösterir
    - Katılımcı bilgilerini gösterir
    - Kayıt durumunu kontrol eder
    """
    
    # Etkinliği getir (bulunamazsa 404 hatası)
    etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)
    
    # Kullanıcının bu etkinliğe kayıtlı olup olmadığını kontrol et
    kullanici_kayitli_mi = False
    if request.user.is_authenticated:
        # Bu kısım kayıtlar uygulaması oluşturulduktan sonra güncellenecek
        # kullanici_kayitli_mi = etkinlik.kayit_set.filter(katilimci=request.user).exists()
        pass
    
    # Benzer etkinlikleri getir (aynı kategoride)
    benzer_etkinlikler = Etkinlik.objects.filter(
        kategori=etkinlik.kategori
    ).exclude(id=etkinlik.id)[:3]
    
    context = {
        'etkinlik': etkinlik,
        'kullanici_kayitli_mi': kullanici_kayitli_mi,
        'benzer_etkinlikler': benzer_etkinlikler,
    }
    
    return render(request, 'etkinlikler/etkinlik_detay.html', context)


@login_required
@organizator_required
def etkinlik_olustur(request):
    """
    Yeni etkinlik oluşturma view'ı (AJAX için)
    
    Bu view sadece POST isteklerini işler ve JSON yanıt döner
    Modal form için optimize edilmiştir
    """
    if request.method == 'POST':
        # Form verilerini al ve doğrula
        form = EtkinlikForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Etkinliği kaydet (organizatör olarak mevcut kullanıcıyı ata)
            etkinlik = form.save(commit=False)
            etkinlik.organizator = request.user
            etkinlik.save()
            
            # Başarı mesajı göster
            messages.success(
                request, 
                f'"{etkinlik.baslik}" etkinliği başarıyla oluşturuldu!'
            )
            
            # Etkinlik detay sayfasına yönlendir
            return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)
        else:
            # Form hatalarını detaylı göster
            error_messages = []
            for field, errors in form.errors.items():
                if field in form.fields:
                    field_name = form.fields[field].label
                    for error in errors:
                        error_messages.append(f"{field_name}: {error}")
                else:
                    # Non-field errors
                    for error in errors:
                        error_messages.append(error)
            
            if error_messages:
                messages.error(request, f'Lütfen aşağıdaki hataları düzeltin: {" | ".join(error_messages)}')
            else:
                messages.error(request, 'Lütfen form hatalarını düzeltin.')
            
            # Hata durumunda ana sayfaya yönlendir (modal kapanır)
            return redirect('etkinlikler:etkinlik_listesi')
    
    # GET istekleri için ana sayfaya yönlendir
    return redirect('etkinlikler:etkinlik_listesi')


@login_required
@organizator_required
def etkinlik_duzenle(request, etkinlik_id):
    """
    Etkinlik düzenleme sayfası
    
    Bu view:
    - Sadece etkinliğin organizatörü düzenleyebilir
    - Mevcut etkinlik bilgilerini form ile gösterir
    - Güncelleme sonrası detay sayfasına yönlendirir
    """
    
    # Etkinliği getir
    etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)
    
    # Sadece organizatör düzenleyebilir
    if etkinlik.organizator != request.user:
        messages.error(request, 'Bu etkinliği düzenleme yetkiniz yok!')
        return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)
    
    if request.method == 'POST':
        # Form verilerini al ve doğrula
        form = EtkinlikForm(request.POST, request.FILES, instance=etkinlik)
        
        if form.is_valid():
            # Etkinliği güncelle
            form.save()
            
            # Başarı mesajı göster
            messages.success(
                request, 
                f'"{etkinlik.baslik}" etkinliği başarıyla güncellendi!'
            )
            
            # Etkinlik detay sayfasına yönlendir
            return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)
        else:
            # Form hatalarını göster
            messages.error(request, 'Lütfen form hatalarını düzeltin.')
            # Hata durumunda detay sayfasına yönlendir
            return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)
    else:
        # GET isteği - detay sayfasına yönlendir (modal form kullanılacak)
        return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)


@login_required
@organizator_required
@require_POST
def etkinlik_sil(request, etkinlik_id):
    """
    Etkinlik silme işlemi
    
    Bu view:
    - Sadece POST isteklerini kabul eder
    - Sadece organizatör silebilir
    - Silme sonrası ana sayfaya yönlendirir
    """
    
    # Etkinliği getir
    etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)
    
    # Sadece organizatör silebilir
    if etkinlik.organizator != request.user:
        messages.error(request, 'Bu etkinliği silme yetkiniz yok!')
        return redirect('etkinlikler:etkinlik_detay', etkinlik_id=etkinlik.id)
    
    # Etkinlik başlığını sakla (mesaj için)
    etkinlik_baslik = etkinlik.baslik
    
    # Etkinliği sil
    etkinlik.delete()
    
    # Başarı mesajı göster
    messages.success(
        request, 
        f'"{etkinlik_baslik}" etkinliği başarıyla silindi!'
    )
    
    # Ana sayfaya yönlendir
    return redirect('etkinlikler:etkinlik_listesi')


def kategori_etkinlikleri(request, kategori_adi):
    """
    Kategori bazında etkinlik listesi
    
    Bu view:
    - Belirli bir kategorideki etkinlikleri gösterir
    - Kategori bulunamazsa 404 hatası verir
    """
    
    # Kategoriyi getir
    kategori = get_object_or_404(Kategori, ad__iexact=kategori_adi)
    
    # Bu kategorideki etkinlikleri getir
    etkinlikler = Etkinlik.objects.filter(kategori=kategori)
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    context = {
        'kategori': kategori,
        'etkinlikler': sayfa,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/kategori_etkinlikleri.html', context)


def etkinlik_ara(request):
    """
    Etkinlik arama sayfası
    
    Bu view:
    - Arama terimine göre etkinlikleri filtreler
    - Başlık, açıklama, yer ve kategori alanlarında arama yapar
    - Kategori ve durum filtrelerini destekler
    """
    
    # URL parametrelerinden filtreleme seçeneklerini al
    arama = request.GET.get('q', '')
    kategori_id = request.GET.get('kategori')
    durum = request.GET.get('durum')
    
    # Etkinlikleri getir
    etkinlikler = Etkinlik.objects.all()
    
    # Arama filtresi
    if arama:
        etkinlikler = etkinlikler.filter(
            Q(baslik__icontains=arama) |
            Q(aciklama__icontains=arama) |
            Q(yer__icontains=arama) |
            Q(kategori__ad__icontains=arama)
        )
    
    # Kategori filtresi
    if kategori_id:
        etkinlikler = etkinlikler.filter(kategori_id=kategori_id)
    
    # Durum filtresi
    if durum:
        etkinlikler = etkinlikler.filter(durum=durum)
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    # Kategorileri getir (filtreleme için)
    kategoriler = Kategori.objects.all()
    
    context = {
        'etkinlikler': sayfa,
        'kategoriler': kategoriler,
        'arama_terimi': arama,
        'secilen_kategori': kategori_id,
        'secilen_durum': durum,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/etkinlik_ara.html', context)


def yaklasan_etkinlikler(request):
    """
    Yaklaşan etkinlikler sayfası
    
    Bu view:
    - Henüz başlamamış etkinlikleri gösterir
    - Tarihe göre sıralar
    """
    
    # Şu andan sonraki etkinlikleri getir
    simdi = timezone.now()
    etkinlikler = Etkinlik.objects.filter(
        baslangic_tarihi__gt=simdi
    ).order_by('baslangic_tarihi')
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    context = {
        'etkinlikler': sayfa,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/yaklasan_etkinlikler.html', context)


def gecmis_etkinlikler(request):
    """
    Geçmiş etkinlikler sayfası
    
    Bu view:
    - Tamamlanmış etkinlikleri gösterir
    - Tarihe göre sıralar
    """
    
    # Şu andan önceki etkinlikleri getir
    simdi = timezone.now()
    etkinlikler = Etkinlik.objects.filter(
        bitis_tarihi__lt=simdi
    ).order_by('-baslangic_tarihi')
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    context = {
        'etkinlikler': sayfa,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/gecmis_etkinlikler.html', context)


def organizator_etkinlikleri(request, username):
    """
    Organizatörün etkinlikleri sayfası
    
    Bu view:
    - Belirli bir organizatörün etkinliklerini gösterir
    - Kullanıcı bulunamazsa 404 hatası verir
    """
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Kullanıcıyı getir
    organizator = get_object_or_404(User, username=username)
    
    # Bu organizatörün etkinliklerini getir
    etkinlikler = Etkinlik.objects.filter(organizator=organizator)
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    context = {
        'organizator': organizator,
        'etkinlikler': sayfa,
        'toplam_etkinlik': etkinlikler.count(),
    }
    
    return render(request, 'etkinlikler/organizator_etkinlikleri.html', context)


def yakindaki_etkinlikler(request):
    """
    Kullanıcının konumuna yakın etkinlikleri gösterir (sadece yerel etkinlikler)
    """
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = int(request.GET.get('radius', 10))

    etkinlikler = Etkinlik.objects.filter(durum='aktif').order_by('-baslangic_tarihi')[:12]
    context = {
        'etkinlikler': etkinlikler,
        'konum_belirtilmedi': not (lat and lng),
        'radius': radius,
    }
    return render(request, 'etkinlikler/yakindaki_etkinlikler.html', context)


def yakindaki_etkinlikler_api(request):
    """
    Yakındaki etkinlikleri JSON formatında döndürür (sadece yerel etkinlikler)
    """
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = int(request.GET.get('radius', 10))

    local_events = Etkinlik.objects.filter(durum='aktif').values('id', 'baslik', 'aciklama', 'yer', 'baslangic_tarihi', 'ucret')
    results = {
        'local_events': list(local_events),
        'user_location': {'lat': lat, 'lng': lng},
        'radius': radius,
        'total_count': local_events.count()
    }
    return JsonResponse(results)

# eventbrite_sync fonksiyonu tamamen kaldırıldı 