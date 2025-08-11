# =============================================================================
# ÖRNEK VERİ OLUŞTURMA KOMUTU
# =============================================================================
# Bu komut projeyi test etmek için örnek veriler oluşturur
# Kullanım: python manage.py create_sample_data

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from etkinlikler.models import Etkinlik, Kategori
from katilimcilar.models import Katilimci
from organizatorler.models import Organizator
from kayitlar.models import Kayit

class Command(BaseCommand):
    help = 'Proje için örnek veriler oluşturur (etkinlikler, kategoriler, kullanıcılar)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Mevcut örnek verileri temizler',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Oluşturulacak etkinlik sayısı (varsayılan: 20)',
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.clear_sample_data()
        
        self.stdout.write(
            self.style.SUCCESS('🎯 Örnek veriler oluşturuluyor...')
        )
        
        # Kategoriler oluştur
        kategoriler = self.create_categories()
        
        # Kullanıcılar ve organizatörler oluştur
        organizatorler = self.create_organizators()
        
        # Etkinlikler oluştur
        etkinlikler = self.create_events(kategoriler, organizatorler, options['count'])
        
        # Katılımcılar oluştur
        katilimcilar = self.create_participants()
        
        # Kayıtlar oluştur
        self.create_registrations(etkinlikler, katilimcilar)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {options["count"]} etkinlik ve örnek veriler başarıyla oluşturuldu!')
        )
    
    def create_categories(self):
        """Kategoriler oluşturur"""
        kategoriler_data = [
            {'ad': 'Konser', 'aciklama': 'Müzik konserleri ve festivaller', 'icon': '🎵'},
            {'ad': 'Tiyatro', 'aciklama': 'Tiyatro oyunları ve performanslar', 'icon': '🎭'},
            {'ad': 'Spor', 'aciklama': 'Spor etkinlikleri ve turnuvalar', 'icon': '⚽'},
            {'ad': 'Seminer', 'aciklama': 'Eğitim ve bilgi paylaşım etkinlikleri', 'icon': '📚'},
            {'ad': 'Yemek', 'aciklama': 'Yemek festivalleri ve workshop\'lar', 'icon': '🍕'},
            {'ad': 'Teknoloji', 'aciklama': 'Teknoloji konferansları ve hackathon\'lar', 'icon': '💻'},
            {'ad': 'Sanat', 'aciklama': 'Sanat sergileri ve workshop\'lar', 'icon': '🎨'},
            {'ad': 'İş', 'aciklama': 'İş ve networking etkinlikleri', 'icon': '💼'},
            {'ad': 'Eğitim', 'aciklama': 'Eğitim ve gelişim etkinlikleri', 'icon': '🎓'},
            {'ad': 'Sağlık', 'aciklama': 'Sağlık ve wellness etkinlikleri', 'icon': '🏥'},
        ]
        
        kategoriler = []
        for data in kategoriler_data:
            kategori, created = Kategori.objects.get_or_create(
                ad=data['ad'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  �� Kategori oluşturuldu: {kategori.ad}')
            kategoriler.append(kategori)
        
        return kategoriler
    
    
    def create_organizators(self):
        """Organizatörler oluşturur"""
        organizator_data = [
            {'username': 'organizator1', 'email': 'org1@example.com', 'first_name': 'Ahmet', 'last_name': 'Yılmaz'},
            {'username': 'organizator2', 'email': 'org2@example.com', 'first_name': 'Ayşe', 'last_name': 'Demir'},
            {'username': 'organizator3', 'email': 'org3@example.com', 'first_name': 'Mehmet', 'last_name': 'Kaya'},
            {'username': 'organizator4', 'email': 'org4@example.com', 'first_name': 'Fatma', 'last_name': 'Özkan'},
            {'username': 'organizator5', 'email': 'org5@example.com', 'first_name': 'Ali', 'last_name': 'Çelik'},
        ]
        
        organizatorler = []
        for data in organizator_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_staff': True,
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'  👤 Kullanıcı oluşturuldu: {user.username}')
            
            organizator, created = Organizator.objects.get_or_create(
                user=user,
                defaults={
                    'telefon': f'+90555{random.randint(1000000, 9999999)}',
                    'adres': f'{data["first_name"]} {data["last_name"]} Adres',
                    'website': f'https://{data["username"]}.com',
                    'bio': f'{data["first_name"]} {data["last_name"]} organizatör profili',  # aciklama -> bio
                    'organizasyon_adi': f'{data["first_name"]} Organizasyon',  # Eksik alan eklendi
                    'pozisyon': 'Organizatör'  # Eksik alan eklendi
                }
            )
            if created:
                self.stdout.write(f'  🎪 Organizatör oluşturuldu: {organizator.user.username}')
            organizatorler.append(organizator)
        
        return organizatorler
    
    def create_events(self, kategoriler, organizatorler, count):
        """Etkinlikler oluşturur"""
        etkinlik_basliklari = [
            'Yaz Konseri', 'Rock Festivali', 'Jazz Gecesi', 'Klasik Müzik Konseri',
            'Tiyatro Oyunu', 'Dans Performansı', 'Stand-up Gösterisi', 'Çocuk Tiyatrosu',
            'Futbol Turnuvası', 'Basketbol Maçı', 'Yüzme Yarışması', 'Koşu Etkinliği',
            'Teknoloji Konferansı', 'Startup Demo Günü', 'Hackathon', 'AI Workshop',
            'Yemek Festivali', 'Şarap Tadımı', 'Kahve Workshop', 'Pasta Yapımı',
            'Sanat Sergisi', 'Fotoğraf Workshop', 'Resim Atölyesi', 'El Sanatları',
            'İş Networking', 'Kariyer Fuarı', 'Mentorluk Programı', 'Girişimcilik Semineri'
        ]
        
        yerler = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep']
        
        etkinlikler = []
        for i in range(count):
            # Rastgele tarih (gelecek 30 gün içinde)
            baslangic_tarihi = timezone.now() + timedelta(days=random.randint(1, 30))
            bitis_tarihi = baslangic_tarihi + timedelta(hours=random.randint(2, 8))
            
            # Organizatör seç ve User instance'ını al
            organizator = random.choice(organizatorler)
            
            etkinlik = Etkinlik.objects.create(
                baslik=f"{random.choice(etkinlik_basliklari)} {i+1}",
                aciklama=f"Bu, {i+1}. örnek etkinliktir. Detaylı açıklama burada yer alır.",
                kategori=random.choice(kategoriler),
                organizator=organizator.user,  # organizator.user kullan (User instance)
                yer=random.choice(yerler),
                baslangic_tarihi=baslangic_tarihi,
                bitis_tarihi=bitis_tarihi,
                maksimum_katilimci=random.randint(50, 500),  # kapasite -> maksimum_katilimci
                ucret=random.choice([0, 25, 50, 75, 100, 150, 200]),
                durum=random.choice(['planlandi', 'aktif', 'tamamlandi']),
                adres=f"Detaylı adres: Bu etkinlik {random.choice(yerler)} şehrinde gerçekleşecek."  # aciklama_detay -> adres
            )
            etkinlikler.append(etkinlik)
            self.stdout.write(f'  �� Etkinlik oluşturuldu: {etkinlik.baslik}')
        
        return etkinlikler
    
    def create_participants(self):
        """Katılımcılar oluşturur"""
        katilimci_data = [
            {'username': 'katilimci1', 'email': 'kat1@example.com', 'first_name': 'Can', 'last_name': 'Arslan'},
            {'username': 'katilimci2', 'email': 'kat2@example.com', 'first_name': 'Elif', 'last_name': 'Yıldız'},
            {'username': 'katilimci3', 'email': 'kat3@example.com', 'first_name': 'Burak', 'last_name': 'Özkan'},
            {'username': 'katilimci4', 'email': 'kat4@example.com', 'first_name': 'Zeynep', 'last_name': 'Kaya'},
            {'username': 'katilimci5', 'email': 'kat5@example.com', 'first_name': 'Deniz', 'last_name': 'Demir'},
            {'username': 'katilimci6', 'email': 'kat6@example.com', 'first_name': 'Mert', 'last_name': 'Çelik'},
            {'username': 'katilimci7', 'email': 'kat7@example.com', 'first_name': 'Selin', 'last_name': 'Arıkan'},
            {'username': 'katilimci8', 'email': 'kat8@example.com', 'first_name': 'Kaan', 'last_name': 'Yılmaz'},
        ]
        
        katilimcilar = []
        for data in katilimci_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'  Katılımcı kullanıcısı oluşturuldu: {user.username}')
            
            katilimci, created = Katilimci.objects.get_or_create(
                user=user,
                defaults={
                    'telefon': f'+90555{random.randint(1000000, 9999999)}',
                    'adres': f'{data["first_name"]} {data["last_name"]} Adres',
                    'dogum_tarihi': f'{random.randint(1980, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                    'sehir': random.choice(['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya']),  # cinsiyet -> sehir
                    'bio': f'{data["first_name"]} {data["last_name"]} katılımcı profili',  # meslek -> bio
                    'website': f'https://{data["username"]}.com'  # Eksik alan eklendi
                }
            )
            if created:
                self.stdout.write(f'  🎫 Katılımcı oluşturuldu: {katilimci.user.username}')
            katilimcilar.append(katilimci)
        
        return katilimcilar
    

    # ... existing code ...

    def create_registrations(self, etkinlikler, katilimcilar):
        """Kayıtlar oluşturur"""
        durumlar = ['beklemede', 'onaylandi', 'reddedildi', 'iptal_edildi']  # Düzeltildi
        
        for etkinlik in etkinlikler:
            # Her etkinlik için rastgele sayıda kayıt oluştur
            kayit_sayisi = random.randint(5, min(etkinlik.maksimum_katilimci, 50))
            
            for _ in range(kayit_sayisi):
                katilimci = random.choice(katilimcilar)
                durum = random.choice(durumlar)
                
                kayit, created = Kayit.objects.get_or_create(
                    etkinlik=etkinlik,
                    katilimci=katilimci.user,  # katilimci.user kullan (User instance)
                    defaults={
                        'durum': durum,
                        'kayit_tarihi': timezone.now(),
                        'notlar': f'Örnek kayıt notu - {durum} durumunda',
                        'kayit_turu': random.choice(['normal', 'vip', 'erken_kayit', 'indirimli']),  # Eksik alan
                        'odendi': random.choice([True, False])  # Eksik alan
                    }
                )
                
                if created:
                    self.stdout.write(f'  Kayıt oluşturuldu: {katilimci.user.username} -> {etkinlik.baslik}')

# ... existing code ...

    
    def clear_sample_data(self):
        """Örnek verileri temizler"""
        self.stdout.write(
            self.style.WARNING('UYARI: Örnek veriler temizleniyor...')
        )
        
        # Kayıtları temizle
        Kayit.objects.all().delete()
        self.stdout.write('  - Kayıtlar temizlendi')
        
        # Etkinlikleri temizle
        Etkinlik.objects.all().delete()
        self.stdout.write('  - Etkinlikler temizlendi')
        
        # Kategorileri temizle
        Kategori.objects.all().delete()
        self.stdout.write('  - Kategoriler temizlendi')
        
        # Katılımcıları temizle
        Katilimci.objects.all().delete()
        self.stdout.write('  - Katılımcılar temizlendi')
        
        # Organizatörleri temizle
        Organizator.objects.all().delete()
        self.stdout.write('  - Organizatörler temizlendi')
        
        # Test kullanıcılarını temizle
        User.objects.filter(username__startswith='test').delete()
        User.objects.filter(username__startswith='organizator').delete()
        User.objects.filter(username__startswith='katilimci').delete()
        self.stdout.write('  - Test kullanıcıları temizlendi')
        
        self.stdout.write(
            self.style.SUCCESS('BASARILI: Tüm örnek veriler temizlendi!')
        )