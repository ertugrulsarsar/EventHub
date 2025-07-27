# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - VIEW FONKSİYONLARI
# =============================================================================
# Bu dosya HTTP isteklerini işleyen view fonksiyonlarını içerir

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Organizator
from .forms import OrganizatorProfilForm, UserProfilForm
from etkinlikler.models import Etkinlik


@login_required
def profil(request):
    """
    Organizatör profil sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının profil bilgilerini gösterir
    - Etkinlik istatistiklerini gösterir
    """
    
    # Organizatör bilgilerini getir
    organizator, created = Organizator.objects.get_or_create(user=request.user)
    
    # Etkinlik istatistikleri
    etkinlikler = Etkinlik.objects.filter(organizator=request.user)
    toplam_etkinlik = etkinlikler.count()
    aktif_etkinlik = etkinlikler.filter(durum='aktif').count()
    tamamlanan_etkinlik = etkinlikler.filter(durum='tamamlandi').count()
    
    # Son etkinlikler
    son_etkinlikler = etkinlikler.order_by('-olusturma_tarihi')[:5]
    
    context = {
        'organizator': organizator,
        'toplam_etkinlik': toplam_etkinlik,
        'aktif_etkinlik': aktif_etkinlik,
        'tamamlanan_etkinlik': tamamlanan_etkinlik,
        'etkinlikler': son_etkinlikler  # Template'de 'etkinlikler' olarak kullanılıyor
    }
    
    return render(request, 'organizatorler/profil.html', context)


@login_required
def etkinliklerim(request):
    """
    Organizatörün etkinlikleri sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının etkinliklerini listeler
    - Sayfalama yapar
    - Filtreleme seçenekleri sunar
    """
    
    # Etkinlikleri getir
    etkinlikler = Etkinlik.objects.filter(organizator=request.user).order_by('-olusturma_tarihi')
    
    # Durum filtresi
    durum = request.GET.get('durum')
    if durum:
        etkinlikler = etkinlikler.filter(durum=durum)
    
    # Sayfalama
    paginator = Paginator(etkinlikler, 12)
    sayfa_numarasi = request.GET.get('sayfa')
    sayfa = paginator.get_page(sayfa_numarasi)
    
    context = {
        'etkinlikler': sayfa,
        'toplam_etkinlik': etkinlikler.count(),
        'durum_secili': durum
    }
    
    return render(request, 'organizatorler/etkinliklerim.html', context)


def kayit(request):
    """
    Organizatör kayıt sayfası
    
    Bu view:
    - Yeni organizatör kaydı oluşturur
    - Kullanıcı hesabı ve organizatör profili oluşturur
    """
    
    if request.method == 'POST':
        # Form verilerini al
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Şifre kontrolü
        if password1 != password2:
            messages.error(request, 'Şifreler eşleşmiyor!')
            return render(request, 'organizatorler/kayit.html')
        
        # Kullanıcı adı kontrolü
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor!')
            return render(request, 'organizatorler/kayit.html')
        
        # E-posta kontrolü
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Bu e-posta adresi zaten kullanılıyor!')
            return render(request, 'organizatorler/kayit.html')
        
        try:
            # Kullanıcı oluştur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Organizatör profili oluştur
            Organizator.objects.create(user=user)
            
            messages.success(request, 'Kayıt başarıyla oluşturuldu! Giriş yapabilirsiniz.')
            return redirect('etkinlikler:etkinlik_listesi')
            
        except Exception as e:
            messages.error(request, f'Kayıt oluşturulurken hata: {str(e)}')
    
    return render(request, 'organizatorler/kayit.html')


@login_required
def profil_duzenle(request):
    """
    Organizatör profil düzenleme sayfası
    
    Bu view:
    - Giriş yapmış kullanıcının profil bilgilerini düzenler
    - Hem kullanıcı hem organizatör bilgilerini günceller
    """
    
    # Organizatör bilgilerini getir
    organizator, created = Organizator.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Form verilerini al
        user_form = UserProfilForm(request.POST, instance=request.user)
        organizator_form = OrganizatorProfilForm(request.POST, request.FILES, instance=organizator)
        
        if user_form.is_valid() and organizator_form.is_valid():
            # Kullanıcı bilgilerini kaydet
            user_form.save()
            
            # Organizatör bilgilerini kaydet
            organizator_form.save()
            
            messages.success(request, 'Profil başarıyla güncellendi!')
            return redirect('organizatorler:profil')
        else:
            # Form hatalarını göster
            if user_form.errors:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{user_form.fields[field].label}: {error}')
            
            if organizator_form.errors:
                for field, errors in organizator_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{organizator_form.fields[field].label}: {error}')
    else:
        # GET isteği - mevcut bilgilerle form göster
        user_form = UserProfilForm(instance=request.user)
        organizator_form = OrganizatorProfilForm(instance=organizator)
    
    context = {
        'user_form': user_form,
        'organizator_form': organizator_form,
        'organizator': organizator
    }
    
    return render(request, 'organizatorler/profil_duzenle.html', context)





def login_view(request):
    """
    Kullanıcı giriş işlemi (AJAX için)
    
    Bu view:
    - Kullanıcı girişi yapar
    - AJAX istekleri için JSON yanıt döner
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Kullanıcı türüne göre yönlendirme
                try:
                    # Organizatör kontrolü
                    organizator = Organizator.objects.get(user=user)
                    return JsonResponse({
                        'success': True,
                        'message': f'Hoş geldiniz, Organizatör {user.first_name or user.username}!',
                        'redirect_url': '/organizatorler/profil/'
                    })
                except Organizator.DoesNotExist:
                    # Katılımcı kontrolü
                    try:
                        from katilimcilar.models import Katilimci
                        katilimci = Katilimci.objects.get(user=user)
                        return JsonResponse({
                            'success': True,
                            'message': f'Hoş geldiniz, {user.first_name or user.username}!',
                            'redirect_url': '/'
                        })
                    except:
                        # Hiçbir profili yoksa ana sayfaya yönlendir
                        return JsonResponse({
                            'success': True,
                            'message': f'Hoş geldiniz, {user.first_name or user.username}!',
                            'redirect_url': '/'
                        })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Kullanıcı adı veya şifre hatalı!'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Lütfen tüm alanları doldurun!'
            })
    
    # GET isteği - ana sayfaya yönlendir
    return redirect('etkinlikler:etkinlik_listesi')


def logout_view(request):
    """
    Kullanıcı çıkış işlemi
    
    Bu view:
    - Kullanıcıyı sistemden çıkarır
    - Ana sayfaya yönlendirir
    - Başarı mesajı gösterir
    """
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız!')
    return redirect('etkinlikler:etkinlik_listesi')