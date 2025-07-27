# =============================================================================
# KATILIMCILAR UYGULAMASI - VIEW FONKSİYONLARI
# =============================================================================
# Bu dosya HTTP isteklerini işleyen view fonksiyonlarını içerir

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
from .models import Katilimci


def katilimci_listesi(request):
    """
    Katılımcı listesi sayfası
    
    Bu view:
    - Tüm katılımcıları listeler
    - Arama ve filtreleme özellikleri sunar
    """
    
    # Arama parametresi
    q = request.GET.get('q', '')
    
    # Katılımcıları getir
    katilimcilar = Katilimci.objects.all()
    
    # Arama yap
    if q:
        katilimcilar = katilimcilar.filter(
            user__username__icontains=q
        ) | katilimcilar.filter(
            user__first_name__icontains=q
        ) | katilimcilar.filter(
            user__last_name__icontains=q
        ) | katilimcilar.filter(
            user__email__icontains=q
        )
    
    context = {
        'katilimcilar': katilimcilar,
        'arama_terimi': q
    }
    
    return render(request, 'katilimcilar/katilimci_listesi.html', context)


def katilimci_detay(request, katilimci_id):
    """
    Katılımcı detay sayfası
    
    Bu view:
    - Belirli bir katılımcının detaylarını gösterir
    - Katılımcının etkinlik geçmişini gösterir
    """
    
    katilimci = get_object_or_404(Katilimci, id=katilimci_id)
    
    context = {
        'katilimci': katilimci
    }
    
    return render(request, 'katilimcilar/katilimci_detay.html', context)


@login_required
def profil(request):
    """
    Katılımcı profil sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının profil bilgilerini gösterir
    - Katılım istatistiklerini gösterir
    """
    
    # Katılımcı bilgilerini getir (yoksa oluştur)
    katilimci, created = Katilimci.objects.get_or_create(user=request.user)
    
    # Katılım istatistiklerini hesapla
    from kayitlar.models import Kayit
    katilimlarim_sayisi = Kayit.objects.filter(katilimci=request.user).count()
    aktif_katilimlar = Kayit.objects.filter(
        katilimci=request.user,
        etkinlik__durum='aktif'
    ).count()
    
    context = {
        'katilimci': katilimci,
        'user': request.user,
        'katilimlarim_sayisi': katilimlarim_sayisi,
        'aktif_katilimlar': aktif_katilimlar
    }
    
    return render(request, 'katilimcilar/profil.html', context)


@login_required
def profil_duzenle(request):
    """
    Katılımcı profil düzenleme sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının profil bilgilerini düzenler
    - Hem kullanıcı hem katılımcı bilgilerini günceller
    """
    
    # Katılımcı bilgilerini getir
    katilimci, created = Katilimci.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Kullanıcı bilgilerini güncelle
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Katılımcı bilgilerini güncelle
        katilimci.telefon = request.POST.get('telefon', '')
        katilimci.dogum_tarihi = request.POST.get('dogum_tarihi', '') or None
        katilimci.adres = request.POST.get('adres', '')
        katilimci.sehir = request.POST.get('sehir', '')
        katilimci.bio = request.POST.get('bio', '')
        katilimci.website = request.POST.get('website', '')
        katilimci.linkedin = request.POST.get('linkedin', '')
        katilimci.twitter = request.POST.get('twitter', '')
        katilimci.email_bildirim = 'email_bildirim' in request.POST
        katilimci.sms_bildirim = 'sms_bildirim' in request.POST
        
        # Profil resmi kontrolü
        if 'profil_resmi' in request.FILES:
            katilimci.profil_resmi = request.FILES['profil_resmi']
        
        katilimci.save()
        
        messages.success(request, 'Profil başarıyla güncellendi!')
        return redirect('katilimcilar:profil')
    
    context = {
        'katilimci': katilimci,
        'user': request.user
    }
    
    return render(request, 'katilimcilar/profil_duzenle.html', context)


def kayit(request):
    """
    Katılımcı kayıt işlemi (AJAX için)
    
    Bu view:
    - Yeni katılımcı kaydı oluşturur
    - AJAX istekleri için JSON yanıt döner
    """
    
    if request.method == 'POST':
        # Form verilerini al
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')  # Boş string varsayılan değer
        
        # Şifre kontrolü
        if password1 != password2:
            return JsonResponse({
                'success': False,
                'message': 'Şifreler eşleşmiyor!'
            })
        
        # Kullanıcı adı kontrolü
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Bu kullanıcı adı zaten kullanılıyor!'
            })
        
        # E-posta kontrolü
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Bu e-posta adresi zaten kullanılıyor!'
            })
        
        try:
            # Kullanıcı oluştur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Katılımcı profili oluştur
            Katilimci.objects.create(user=user)
            
            return JsonResponse({
                'success': True,
                'message': 'Kayıt başarıyla oluşturuldu! Giriş yapabilirsiniz.',
                'show_login_modal': True
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Kayıt oluşturulurken hata: {str(e)}'
            })
    
    # GET isteği - ana sayfaya yönlendir
    return redirect('etkinlikler:etkinlik_listesi') 