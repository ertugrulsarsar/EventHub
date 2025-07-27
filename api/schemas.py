# =============================================================================
# API - PYDANTIC ŞEMALARI
# =============================================================================
# Bu dosya FastAPI için Pydantic şemalarını tanımlar
# API request/response modellerini belirler

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# =============================================================================
# KATEGORİ ŞEMALARI
# =============================================================================

class KategoriBase(BaseModel):
    """Kategori temel şeması"""
    ad: str = Field(..., description="Kategori adı", max_length=100)
    aciklama: Optional[str] = Field(None, description="Kategori açıklaması")
    icon: Optional[str] = Field("calendar-event", description="Bootstrap icon adı", max_length=50)


class KategoriCreate(KategoriBase):
    """Kategori oluşturma şeması"""
    pass


class KategoriUpdate(KategoriBase):
    """Kategori güncelleme şeması"""
    ad: Optional[str] = Field(None, description="Kategori adı", max_length=100)


class Kategori(KategoriBase):
    """Kategori response şeması"""
    id: int
    olusturma_tarihi: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# ETKİNLİK ŞEMALARI
# =============================================================================

class EtkinlikBase(BaseModel):
    """Etkinlik temel şeması"""
    baslik: str = Field(..., description="Etkinlik başlığı", max_length=200)
    aciklama: Optional[str] = Field(None, description="Etkinlik açıklaması")
    baslangic_tarihi: datetime = Field(..., description="Başlangıç tarihi ve saati")
    bitis_tarihi: datetime = Field(..., description="Bitiş tarihi ve saati")
    yer: str = Field(..., description="Etkinlik yeri", max_length=200)
    adres: Optional[str] = Field(None, description="Detaylı adres")
    maksimum_katilimci: int = Field(100, description="Maksimum katılımcı sayısı", ge=1)
    durum: str = Field("planlandi", description="Etkinlik durumu")
    ucret: Optional[float] = Field(None, description="Etkinlik ücreti", ge=0)


class EtkinlikCreate(EtkinlikBase):
    """Etkinlik oluşturma şeması"""
    kategori_id: int = Field(..., description="Kategori ID'si")
    organizator_id: int = Field(..., description="Organizatör ID'si")


class EtkinlikUpdate(EtkinlikBase):
    """Etkinlik güncelleme şeması"""
    baslik: Optional[str] = Field(None, description="Etkinlik başlığı", max_length=200)
    baslangic_tarihi: Optional[datetime] = Field(None, description="Başlangıç tarihi ve saati")
    bitis_tarihi: Optional[datetime] = Field(None, description="Bitiş tarihi ve saati")
    yer: Optional[str] = Field(None, description="Etkinlik yeri", max_length=200)
    maksimum_katilimci: Optional[int] = Field(None, description="Maksimum katılımcı sayısı", ge=1)
    kategori_id: Optional[int] = Field(None, description="Kategori ID'si")


class Etkinlik(EtkinlikBase):
    """Etkinlik response şeması"""
    id: int
    kategori_id: int
    organizator_id: int
    mevcut_katilimci: int
    resim: Optional[str] = None
    olusturma_tarihi: datetime
    guncelleme_tarihi: datetime
    kategori: Optional[Kategori] = None
    
    class Config:
        from_attributes = True


# =============================================================================
# KATILIMCI ŞEMALARI
# =============================================================================

class KatilimciBase(BaseModel):
    """Katılımcı temel şeması"""
    telefon: Optional[str] = Field(None, description="Telefon numarası", max_length=15)
    dogum_tarihi: Optional[date] = Field(None, description="Doğum tarihi")
    adres: Optional[str] = Field(None, description="Adres bilgisi")
    sehir: Optional[str] = Field(None, description="Şehir", max_length=50)
    bio: Optional[str] = Field(None, description="Hakkında bilgisi")
    website: Optional[str] = Field(None, description="Website adresi", max_length=200)
    linkedin: Optional[str] = Field(None, description="LinkedIn profili", max_length=200)
    twitter: Optional[str] = Field(None, description="Twitter profili", max_length=200)
    email_bildirim: bool = Field(True, description="E-posta bildirimleri")
    sms_bildirim: bool = Field(False, description="SMS bildirimleri")


class KatilimciCreate(KatilimciBase):
    """Katılımcı oluşturma şeması"""
    user_id: int = Field(..., description="Kullanıcı ID'si")


class KatilimciUpdate(KatilimciBase):
    """Katılımcı güncelleme şeması"""
    pass


class Katilimci(KatilimciBase):
    """Katılımcı response şeması"""
    id: int
    user_id: int
    profil_resmi: Optional[str] = None
    kayit_tarihi: datetime
    son_guncelleme: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# KAYIT ŞEMALARI
# =============================================================================

class KayitBase(BaseModel):
    """Kayıt temel şeması"""
    durum: str = Field("beklemede", description="Kayıt durumu")
    kayit_turu: str = Field("normal", description="Kayıt türü")
    odendi: bool = Field(False, description="Ödeme durumu")
    odeme_yontemi: Optional[str] = Field(None, description="Ödeme yöntemi", max_length=50)
    notlar: Optional[str] = Field(None, description="Ek notlar")


class KayitCreate(KayitBase):
    """Kayıt oluşturma şeması"""
    katilimci_id: int = Field(..., description="Katılımcı ID'si")
    etkinlik_id: int = Field(..., description="Etkinlik ID'si")


class KayitUpdate(KayitBase):
    """Kayıt güncelleme şeması"""
    durum: Optional[str] = Field(None, description="Kayıt durumu")
    kayit_turu: Optional[str] = Field(None, description="Kayıt türü")
    odendi: Optional[bool] = Field(None, description="Ödeme durumu")


class Kayit(KayitBase):
    """Kayıt response şeması"""
    id: int
    katilimci_id: int
    etkinlik_id: int
    odeme_tarihi: Optional[datetime] = None
    kayit_tarihi: datetime
    guncelleme_tarihi: datetime
    katilimci: Optional[Katilimci] = None
    etkinlik: Optional[Etkinlik] = None
    
    class Config:
        from_attributes = True


# =============================================================================
# ORGANİZATÖR ŞEMALARI
# =============================================================================

class OrganizatorBase(BaseModel):
    """Organizatör temel şeması"""
    telefon: Optional[str] = Field(None, description="Telefon numarası", max_length=15)
    organizasyon_adi: Optional[str] = Field(None, description="Organizasyon adı", max_length=100)
    pozisyon: Optional[str] = Field(None, description="Pozisyon", max_length=100)
    website: Optional[str] = Field(None, description="Website adresi", max_length=200)
    adres: Optional[str] = Field(None, description="Adres bilgisi")
    bio: Optional[str] = Field(None, description="Hakkında bilgisi")
    linkedin: Optional[str] = Field(None, description="LinkedIn profili", max_length=200)
    twitter: Optional[str] = Field(None, description="Twitter profili", max_length=200)
    is_verified: bool = Field(False, description="Doğrulanmış hesap")
    is_premium: bool = Field(False, description="Premium üye")


class OrganizatorCreate(OrganizatorBase):
    """Organizatör oluşturma şeması"""
    user_id: int = Field(..., description="Kullanıcı ID'si")


class OrganizatorUpdate(OrganizatorBase):
    """Organizatör güncelleme şeması"""
    pass


class Organizator(OrganizatorBase):
    """Organizatör response şeması"""
    id: int
    user_id: int
    profil_resmi: Optional[str] = None
    kayit_tarihi: datetime
    son_guncelleme: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# GENEL ŞEMALAR
# =============================================================================

class Message(BaseModel):
    """Mesaj şeması"""
    message: str
    success: bool = True


class Stats(BaseModel):
    """İstatistik şeması"""
    etkinlik_sayisi: int
    katilimci_sayisi: int
    kayit_sayisi: int
    onayli_kayit_sayisi: int


class PaginatedResponse(BaseModel):
    """Sayfalanmış response şeması"""
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int 