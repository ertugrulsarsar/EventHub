# =============================================================================
# KAYITLAR UYGULAMASI - VIEW FONKSİYONLARI
# =============================================================================
# Bu dosya HTTP isteklerini işleyen view fonksiyonlarını içerir

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Kayit
from etkinlikler.models import Etkinlik


def kayit_listesi(request):
    """
    Kayıt listesi sayfası
    
    Bu view:
    - Tüm kayıtları listeler (sadece admin için)
    - Arama ve filtreleme özellikleri sunar
    """
    
    # Sadece admin kullanıcılar erişebilir
    if not request.user.is_staff:
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok!')
        return redirect('etkinlikler:etkinlik_listesi')
    
    # Arama parametreleri
    q = request.GET.get('q', '')
    durum = request.GET.get('durum', '')
    
    # Kayıtları getir
    kayitlar = Kayit.objects.all()
    
    # Arama yap
    if q:
        kayitlar = kayitlar.filter(
            katilimci__username__icontains=q
        ) | kayitlar.filter(
            etkinlik__baslik__icontains=q
        )
    
    # Durum filtresi
    if durum:
        kayitlar = kayitlar.filter(durum=durum)
    
    context = {
        'kayitlar': kayitlar,
        'arama_terimi': q,
        'secilen_durum': durum
    }
    
    return render(request, 'kayitlar/kayit_listesi.html', context)


def kayit_detay(request, kayit_id):
    """
    Kayıt detay sayfası
    
    Bu view:
    - Belirli bir kaydın detaylarını gösterir
    - Kayıt geçmişini gösterir
    """
    
    kayit = get_object_or_404(Kayit, id=kayit_id)
    
    # Sadece kayıt sahibi veya admin erişebilir
    if not request.user.is_staff and kayit.katilimci != request.user:
        messages.error(request, 'Bu kayda erişim yetkiniz yok!')
        return redirect('kayitlar:katilimlarim')
    
    context = {
        'kayit': kayit
    }
    
    return render(request, 'kayitlar/kayit_detay.html', context)


@login_required
def etkinlik_kayit(request, etkinlik_id):
    """
    Etkinliğe kayıt olma sayfası
    
    Bu view:
    - Kullanıcının etkinliğe kayıt olmasını sağlar
    - Kayıt türü ve ödeme bilgilerini alır
    """
    
    etkinlik = get_object_or_404(Etkinlik, id=etkinlik_id)
    
    # Etkinlik aktif mi kontrol et
    if not etkinlik.etkinlik_aktif_mi():
        messages.error(request, 'Bu etkinlik artık kayıt almıyor!')
        return redirect('etkinlikler:etkinlik_detay', etkinlik_id)
    
    # Zaten kayıtlı mı kontrol et
    mevcut_kayit = Kayit.objects.filter(
        katilimci=request.user,
        etkinlik=etkinlik
    ).first()
    
    if mevcut_kayit:
        messages.warning(request, 'Bu etkinliğe zaten kayıtlısınız!')
        return redirect('etkinlikler:etkinlik_detay', etkinlik_id)
    
    if request.method == 'POST':
        # Kayıt türü
        kayit_turu = request.POST.get('kayit_turu', 'normal')
        
        # Notlar
        notlar = request.POST.get('notlar', '')
        
        try:
            # Yeni kayıt oluştur
            kayit = Kayit.objects.create(
                katilimci=request.user,
                etkinlik=etkinlik,
                kayit_turu=kayit_turu,
                notlar=notlar
            )
            
            messages.success(request, 'Etkinliğe başarıyla kayıt oldunuz!')
            return redirect('kayitlar:kayit_detay', kayit.id)
            
        except Exception as e:
            messages.error(request, f'Kayıt oluşturulurken hata: {str(e)}')
    
    context = {
        'etkinlik': etkinlik
    }
    
    return render(request, 'kayitlar/etkinlik_kayit.html', context)


@login_required
def kayit_iptal(request, kayit_id):
    """
    Kayıt iptal etme
    
    Bu view:
    - Kullanıcının kaydını iptal eder
    - Sadece POST isteği ile çalışır
    """
    
    if request.method != 'POST':
        messages.error(request, 'Geçersiz istek!')
        return redirect('kayitlar:katilimlarim')
    
    kayit = get_object_or_404(Kayit, id=kayit_id)
    
    # Sadece kayıt sahibi iptal edebilir
    if kayit.katilimci != request.user:
        messages.error(request, 'Bu kaydı iptal etme yetkiniz yok!')
        return redirect('kayitlar:katilimlarim')
    
    # Kayıt durumunu kontrol et
    if kayit.durum in ['reddedildi', 'iptal_edildi', 'tamamlandi']:
        messages.error(request, 'Bu kayıt zaten iptal edilmiş veya tamamlanmış!')
        return redirect('kayitlar:katilimlarim')
    
    try:
        # Kayıt durumunu iptal olarak değiştir
        kayit.durum = 'iptal_edildi'
        kayit.save()
        
        messages.success(request, 'Kayıt başarıyla iptal edildi!')
        
    except Exception as e:
        messages.error(request, f'Kayıt iptal edilirken hata: {str(e)}')
    
    return redirect('kayitlar:katilimlarim')


@login_required
def katilimlarim(request):
    """
    Kullanıcının katılımları sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının tüm kayıtlarını listeler
    - Kayıt yönetimi seçenekleri sunar
    """
    
    # Kullanıcının kayıtlarını getir
    kayitlar = Kayit.objects.filter(katilimci=request.user).order_by('-kayit_tarihi')
    
    # Durum filtresi
    durum = request.GET.get('durum', '')
    if durum:
        kayitlar = kayitlar.filter(durum=durum)
    
    context = {
        'kayitlar': kayitlar,
        'secilen_durum': durum,
        'toplam_kayit': kayitlar.count(),
        'onayli_kayit': kayitlar.filter(durum='onaylandi').count(),
        'bekleyen_kayit': kayitlar.filter(durum='beklemede').count(),
    }
    
    return render(request, 'kayitlar/katilimlarim.html', context) 