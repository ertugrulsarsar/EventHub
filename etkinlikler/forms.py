# =============================================================================
# ETKİNLİKLER UYGULAMASI - FORM SINIFLARI
# =============================================================================
# Bu dosya etkinlik oluşturma ve düzenleme için form sınıflarını içerir
# Formlar, kullanıcıdan veri almak ve doğrulamak için kullanılır

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Etkinlik, Kategori


class EtkinlikForm(forms.ModelForm):
    """
    Etkinlik oluşturma ve düzenleme formu
    
    Bu form:
    - Etkinlik modelinin tüm alanlarını içerir
    - Özel doğrulama kuralları ekler
    - Bootstrap stilleri ile uyumludur
    """
    
    class Meta:
        """
        Form meta bilgileri
        
        Bu sınıf, formun hangi modeli kullanacağını ve
        hangi alanların görüneceğini belirler
        """
        model = Etkinlik
        
        # Formda görünecek alanlar (organizatör otomatik atanacak)
        fields = [
            'baslik',
            'aciklama', 
            'kategori',
            'baslangic_tarihi',
            'bitis_tarihi',
            'yer',
            'adres',
            'maksimum_katilimci',
            'durum',
            'ucret',
            'resim'
        ]
        
        # Widget'ları özelleştir (Bootstrap stilleri için)
        widgets = {
            'baslik': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Etkinlik başlığını girin...',
                'maxlength': '200'
            }),
            
            'aciklama': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Etkinlik hakkında detaylı açıklama...'
            }),
            
            'kategori': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'baslangic_tarihi': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            
            'bitis_tarihi': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            
            'yer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Etkinlik yeri (örn: Konferans Salonu)',
                'maxlength': '200'
            }),
            
            'adres': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Detaylı adres bilgisi...'
            }),
            
            'maksimum_katilimci': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10000',
                'placeholder': 'Maksimum katılımcı sayısı'
            }),
            
            'durum': forms.Select(attrs={
                'class': 'form-select'
            }),
            
            'ucret': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ücret (ücretsiz ise boş bırakın)'
            }),
            
            'resim': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
        # Alan etiketlerini Türkçe yap
        labels = {
            'baslik': 'Etkinlik Başlığı',
            'aciklama': 'Açıklama',
            'kategori': 'Kategori',
            'baslangic_tarihi': 'Başlangıç Tarihi',
            'bitis_tarihi': 'Bitiş Tarihi',
            'yer': 'Yer',
            'adres': 'Adres',
            'maksimum_katilimci': 'Maksimum Katılımcı',
            'durum': 'Durum',
            'ucret': 'Ücret',
            'resim': 'Etkinlik Resmi'
        }
        
        # Yardım metinleri
        help_texts = {
            'baslik': 'Etkinliğin başlığını girin (maksimum 200 karakter)',
            'aciklama': 'Etkinlik hakkında detaylı açıklama yazın',
            'kategori': 'Etkinliğin kategorisini seçin',
            'baslangic_tarihi': 'Etkinliğin başlayacağı tarih ve saat',
            'bitis_tarihi': 'Etkinliğin biteceği tarih ve saat',
            'yer': 'Etkinliğin yapılacağı yer',
            'adres': 'Etkinlik yerinin detaylı adresi',
            'maksimum_katilimci': 'Etkinliğe katılabilecek maksimum kişi sayısı',
            'durum': 'Etkinliğin mevcut durumu',
            'ucret': 'Etkinlik ücreti (ücretsiz ise boş bırakın)',
            'resim': 'Etkinlik için bir resim yükleyin (isteğe bağlı)'
        }
    
    def __init__(self, *args, **kwargs):
        """
        Form başlatılırken çalışan metod
        
        Bu metod:
        - Kategori seçeneklerini düzenler
        - Durum seçeneklerini düzenler
        - Özel CSS sınıfları ekler
        """
        super().__init__(*args, **kwargs)
        
        # Kategori seçeneklerini düzenle
        self.fields['kategori'].queryset = Kategori.objects.all().order_by('ad')
        
        # Durum seçeneklerini düzenle
        self.fields['durum'].choices = [
            ('', 'Durum seçin...'),  # Boş seçenek ekle
        ] + list(Etkinlik.DURUM_CHOICES)
        
        # Ücret alanını opsiyonel yap
        self.fields['ucret'].required = False
        
        # Resim alanını opsiyonel yap
        self.fields['resim'].required = False
        
        # Adres alanını zorunlu yap
        self.fields['adres'].required = True
        
        # Maksimum katılımcı için varsayılan değer
        if not self.instance.pk:  # Sadece yeni oluşturma için
            self.fields['maksimum_katilimci'].initial = 100
            self.fields['durum'].initial = 'planlandi'
            # Adres için varsayılan değer
            self.fields['adres'].initial = 'Adres bilgisi girilecek'
    
    def clean(self):
        """
        Form verilerini doğrular
        
        Bu metod:
        - Tarih tutarlılığını kontrol eder
        - Kapasite kontrolü yapar
        - Özel doğrulama kuralları uygular
        """
        cleaned_data = super().clean()
        
        # Tarih alanlarını al
        baslangic_tarihi = cleaned_data.get('baslangic_tarihi')
        bitis_tarihi = cleaned_data.get('bitis_tarihi')
        
        # Tarih tutarlılığını kontrol et
        if baslangic_tarihi and bitis_tarihi:
            if baslangic_tarihi >= bitis_tarihi:
                raise ValidationError(
                    'Bitiş tarihi, başlangıç tarihinden sonra olmalıdır!'
                )
            
            # Geçmiş tarih kontrolü (sadece yeni oluşturma için)
            if not self.instance.pk:  # Sadece yeni oluşturma için
                simdi = timezone.now()
                # 1 saat tolerans ver
                if baslangic_tarihi < (simdi - timedelta(hours=1)):
                    raise ValidationError(
                        'Başlangıç tarihi geçmiş bir tarih olamaz!'
                    )
        
        # Kapasite kontrolü
        maksimum_katilimci = cleaned_data.get('maksimum_katilimci')
        if maksimum_katilimci and maksimum_katilimci < 1:
            raise ValidationError(
                'Maksimum katılımcı sayısı en az 1 olmalıdır!'
            )
        
        return cleaned_data
    
    def clean_baslik(self):
        """
        Başlık alanını özel olarak doğrular
        
        Bu metod:
        - Başlığın benzersiz olup olmadığını kontrol eder
        - Başlık formatını kontrol eder
        """
        baslik = self.cleaned_data.get('baslik')
        
        if baslik:
            # Başlık uzunluğunu kontrol et
            if len(baslik.strip()) < 5:
                raise ValidationError(
                    'Başlık en az 5 karakter olmalıdır!'
                )
            
            # Başlığın benzersiz olup olmadığını kontrol et
            # (aynı organizatör için)
            if self.instance.pk:  # Düzenleme modu
                mevcut_etkinlik = Etkinlik.objects.filter(
                    baslik__iexact=baslik,
                    organizator=self.instance.organizator
                ).exclude(pk=self.instance.pk)
            else:  # Yeni oluşturma modu
                # Bu durumda organizatör henüz bilinmiyor
                # View'da kontrol edilecek
                pass
        
        return baslik
    
    def clean_ucret(self):
        """
        Ücret alanını özel olarak doğrular
        
        Bu metod:
        - Ücretin negatif olup olmadığını kontrol eder
        - Ücret formatını kontrol eder
        """
        ucret = self.cleaned_data.get('ucret')
        
        if ucret is not None and ucret < 0:
            raise ValidationError(
                'Ücret negatif olamaz!'
            )
        
        return ucret


class EtkinlikAramaForm(forms.Form):
    """
    Etkinlik arama formu
    
    Bu form:
    - Arama terimi alır
    - Kategori filtresi sunar
    - Tarih aralığı filtresi sunar
    """
    
    # Arama terimi
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Etkinlik ara...',
            'aria-label': 'Arama'
        }),
        label='Arama'
    )
    
    # Kategori filtresi
    kategori = forms.ModelChoiceField(
        queryset=Kategori.objects.all().order_by('ad'),
        required=False,
        empty_label="Tüm Kategoriler",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Kategori'
    )
    
    # Durum filtresi
    durum = forms.ChoiceField(
        choices=[('', 'Tüm Durumlar')] + list(Etkinlik.DURUM_CHOICES),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Durum'
    )
    
    # Tarih aralığı
    baslangic_tarihi = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='Başlangıç Tarihi'
    )
    
    bitis_tarihi = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        label='Bitiş Tarihi'
    )
    
    def clean(self):
        """
        Form verilerini doğrular
        
        Bu metod:
        - Tarih aralığı tutarlılığını kontrol eder
        """
        cleaned_data = super().clean()
        
        baslangic_tarihi = cleaned_data.get('baslangic_tarihi')
        bitis_tarihi = cleaned_data.get('bitis_tarihi')
        
        if baslangic_tarihi and bitis_tarihi:
            if baslangic_tarihi >= bitis_tarihi:
                raise ValidationError(
                    'Bitiş tarihi, başlangıç tarihinden sonra olmalıdır!'
                )
        
        return cleaned_data 