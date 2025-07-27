# =============================================================================
# ÖRNEK VERİ OLUŞTURMA KOMUTU
# =============================================================================
# Bu komut örnek kategoriler ve etkinlikler oluşturur

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from etkinlikler.models import Kategori, Etkinlik
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Örnek kategoriler ve etkinlikler oluşturur'

    def handle(self, *args, **options):
        self.stdout.write('Örnek veriler oluşturuluyor...')
        
        # Kategoriler oluştur
        kategoriler = [
            {'ad': 'Konferans', 'aciklama': 'Bilimsel ve teknik konferanslar', 'icon': 'mic'},
            {'ad': 'Workshop', 'aciklama': 'Pratik eğitim ve atölye çalışmaları', 'icon': 'tools'},
            {'ad': 'Seminer', 'aciklama': 'Eğitici seminerler', 'icon': 'mortarboard'},
            {'ad': 'Konser', 'aciklama': 'Müzik etkinlikleri', 'icon': 'music-note'},
            {'ad': 'Sergi', 'aciklama': 'Sanat ve kültür sergileri', 'icon': 'palette'},
            {'ad': 'Spor', 'aciklama': 'Spor etkinlikleri', 'icon': 'trophy'},
            {'ad': 'Teknoloji', 'aciklama': 'Teknoloji ve yazılım etkinlikleri', 'icon': 'laptop'},
            {'ad': 'İş', 'aciklama': 'İş ve kariyer etkinlikleri', 'icon': 'briefcase'},
        ]
        
        for kategori_data in kategoriler:
            kategori, created = Kategori.objects.get_or_create(
                ad=kategori_data['ad'],
                defaults={
                    'aciklama': kategori_data['aciklama'],
                    'icon': kategori_data['icon']
                }
            )
            if created:
                self.stdout.write(f'Kategori oluşturuldu: {kategori.ad}')
            else:
                self.stdout.write(f'Kategori zaten mevcut: {kategori.ad}')
        
        # Test kullanıcısı oluştur (eğer yoksa)
        test_user, created = User.objects.get_or_create(
            username='test_organizator',
            defaults={
                'first_name': 'Test',
                'last_name': 'Organizatör',
                'email': 'test@example.com',
                'is_staff': True
            }
        )
        if created:
            test_user.set_password('test123')
            test_user.save()
            self.stdout.write('Test kullanıcısı oluşturuldu: test_organizator / test123')
        
        # Örnek etkinlikler oluştur
        etkinlik_verileri = [
            {
                'baslik': 'Python Programlama Workshop',
                'aciklama': 'Python programlama dilini öğrenmek isteyenler için temel workshop.',
                'kategori': 'Workshop',
                'yer': 'Teknoloji Merkezi',
                'adres': 'İstanbul, Türkiye',
                'maksimum_katilimci': 30,
                'ucret': 150.00
            },
            {
                'baslik': 'Web Geliştirme Konferansı',
                'aciklama': 'Modern web teknolojileri hakkında kapsamlı konferans.',
                'kategori': 'Konferans',
                'yer': 'Kongre Merkezi',
                'adres': 'Ankara, Türkiye',
                'maksimum_katilimci': 200,
                'ucret': 300.00
            },
            {
                'baslik': 'Jazz Gecesi',
                'aciklama': 'Yerel jazz sanatçıları ile unutulmaz bir gece.',
                'kategori': 'Konser',
                'yer': 'Jazz Kulübü',
                'adres': 'İzmir, Türkiye',
                'maksimum_katilimci': 100,
                'ucret': 80.00
            },
            {
                'baslik': 'Fotoğraf Sergisi',
                'aciklama': 'Doğa fotoğrafları sergisi.',
                'kategori': 'Sergi',
                'yer': 'Sanat Galerisi',
                'adres': 'Bursa, Türkiye',
                'maksimum_katilimci': 50,
                'ucret': 0.00
            },
            {
                'baslik': 'Futbol Turnuvası',
                'aciklama': 'Amatör futbol takımları turnuvası.',
                'kategori': 'Spor',
                'yer': 'Spor Kompleksi',
                'adres': 'Antalya, Türkiye',
                'maksimum_katilimci': 150,
                'ucret': 25.00
            }
        ]
        
        for i, etkinlik_data in enumerate(etkinlik_verileri):
            kategori = Kategori.objects.get(ad=etkinlik_data['kategori'])
            
            # Gelecek tarihler oluştur
            baslangic_tarihi = datetime.now() + timedelta(days=random.randint(7, 60))
            bitis_tarihi = baslangic_tarihi + timedelta(hours=random.randint(2, 8))
            
            etkinlik, created = Etkinlik.objects.get_or_create(
                baslik=etkinlik_data['baslik'],
                defaults={
                    'aciklama': etkinlik_data['aciklama'],
                    'kategori': kategori,
                    'baslangic_tarihi': baslangic_tarihi,
                    'bitis_tarihi': bitis_tarihi,
                    'yer': etkinlik_data['yer'],
                    'adres': etkinlik_data['adres'],
                    'maksimum_katilimci': etkinlik_data['maksimum_katilimci'],
                    'ucret': etkinlik_data['ucret'],
                    'organizator': test_user,
                    'durum': 'planlandi'
                }
            )
            
            if created:
                self.stdout.write(f'Etkinlik oluşturuldu: {etkinlik.baslik}')
            else:
                self.stdout.write(f'Etkinlik zaten mevcut: {etkinlik.baslik}')
        
        self.stdout.write(
            self.style.SUCCESS('Örnek veriler başarıyla oluşturuldu!')
        )
        self.stdout.write('Test kullanıcısı: test_organizator / test123') 