# =============================================================================
# ORGANİZATÖRLER UYGULAMASI - FORM SINIFLARI
# =============================================================================
# Bu dosya organizatör profil düzenleme için form sınıflarını içerir

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Organizator


class OrganizatorProfilForm(forms.ModelForm):
    """
    Organizatör profil düzenleme formu
    
    Bu form:
    - Organizatör modelinin alanlarını içerir
    - Bootstrap stilleri ile uyumludur
    """
    
    class Meta:
        model = Organizator
        fields = [
            'telefon',
            'organizasyon_adi', 
            'pozisyon',
            'website',
            'adres',
            'bio',
            'linkedin',
            'twitter',
            'profil_resmi'
        ]
        
        widgets = {
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+90 555 123 45 67',
                'maxlength': '20'
            }),
            
            'organizasyon_adi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organizasyon adınız...',
                'maxlength': '100'
            }),
            
            'pozisyon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pozisyonunuz...',
                'maxlength': '100'
            }),
            
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com',
                'maxlength': '200'
            }),
            
            'adres': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Adres bilgileriniz...',
                'maxlength': '500'
            }),
            
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Kendiniz hakkında kısa bilgi...',
                'maxlength': '1000'
            }),
            
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/kullaniciadi',
                'maxlength': '200'
            }),
            
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/kullaniciadi',
                'maxlength': '200'
            }),
            
            'profil_resmi': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
        labels = {
            'telefon': 'Telefon',
            'organizasyon_adi': 'Organizasyon Adı',
            'pozisyon': 'Pozisyon',
            'website': 'Website',
            'adres': 'Adres',
            'bio': 'Hakkımda',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter',
            'profil_resmi': 'Profil Resmi'
        }
        
        help_texts = {
            'telefon': 'Uluslararası formatta telefon numarası girin',
            'website': 'Website adresinizi http:// ile başlayarak girin',
            'linkedin': 'LinkedIn profil adresinizi girin',
            'twitter': 'Twitter profil adresinizi girin',
            'profil_resmi': 'JPG, PNG formatında resim yükleyin (maks. 5MB)'
        }


class UserProfilForm(forms.ModelForm):
    """
    Kullanıcı profil düzenleme formu
    
    Bu form:
    - User modelinin temel alanlarını içerir
    - Şifre değiştirme seçeneği sunar
    """
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mevcut şifrenizi girin...'
        }),
        required=False,
        label='Mevcut Şifre',
        help_text='Şifrenizi değiştirmek istiyorsanız doldurun'
    )
    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifrenizi girin...'
        }),
        required=False,
        label='Yeni Şifre',
        help_text='En az 8 karakter, harf ve rakam içermeli'
    )
    
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifrenizi tekrar girin...'
        }),
        required=False,
        label='Yeni Şifre (Tekrar)',
        help_text='Yeni şifrenizi tekrar girin'
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adınız...',
                'maxlength': '30'
            }),
            
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Soyadınız...',
                'maxlength': '30'
            }),
            
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ornek@email.com',
                'maxlength': '254'
            })
        }
        
        labels = {
            'first_name': 'Ad',
            'last_name': 'Soyad',
            'email': 'E-posta'
        }
        
        help_texts = {
            'first_name': 'Adınızı girin',
            'last_name': 'Soyadınızı girin',
            'email': 'Geçerli bir e-posta adresi girin'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        # Şifre değiştirme kontrolü
        if new_password1 or new_password2:
            if not current_password:
                raise forms.ValidationError('Şifre değiştirmek için mevcut şifrenizi girmelisiniz.')
            
            if not self.instance.check_password(current_password):
                raise forms.ValidationError('Mevcut şifreniz yanlış.')
            
            if new_password1 != new_password2:
                raise forms.ValidationError('Yeni şifreler eşleşmiyor.')
            
            if len(new_password1) < 8:
                raise forms.ValidationError('Yeni şifre en az 8 karakter olmalıdır.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Şifre değiştirme
        if self.cleaned_data.get('new_password1'):
            user.set_password(self.cleaned_data['new_password1'])
        
        if commit:
            user.save()
        
        return user 