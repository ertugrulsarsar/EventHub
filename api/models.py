# =============================================================================
# API - SQLALCHEMY MODELLERİ
# =============================================================================
# Bu dosya FastAPI için SQLAlchemy modellerini tanımlar
# Django modelleri ile uyumlu olacak şekilde tasarlanmıştır

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Kategori(Base):
    """
    Kategori modeli (SQLAlchemy)
    """
    __tablename__ = "etkinlikler_kategori"
    
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String(100), nullable=False)
    aciklama = Column(Text, nullable=True)
    icon = Column(String(50), default="calendar-event")
    olusturma_tarihi = Column(DateTime, default=datetime.now)
    
    # İlişkiler
    etkinlikler = relationship("Etkinlik", back_populates="kategori")


class Etkinlik(Base):
    """
    Etkinlik modeli (SQLAlchemy)
    """
    __tablename__ = "etkinlikler_etkinlik"
    
    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(200), nullable=False)
    aciklama = Column(Text, nullable=True)
    kategori_id = Column(Integer, ForeignKey("etkinlikler_kategori.id"))
    baslangic_tarihi = Column(DateTime, nullable=False)
    bitis_tarihi = Column(DateTime, nullable=False)
    yer = Column(String(200), nullable=False)
    adres = Column(Text, nullable=True)
    maksimum_katilimci = Column(Integer, default=100)
    mevcut_katilimci = Column(Integer, default=0)
    durum = Column(String(20), default="planlandi")
    organizator_id = Column(Integer, ForeignKey("auth_user.id"))
    ucret = Column(Float, nullable=True)
    resim = Column(String(255), nullable=True)
    olusturma_tarihi = Column(DateTime, default=datetime.now)
    guncelleme_tarihi = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # İlişkiler
    kategori = relationship("Kategori", back_populates="etkinlikler")
    kayitlar = relationship("Kayit", back_populates="etkinlik")


class Katilimci(Base):
    """
    Katılımcı modeli (SQLAlchemy)
    """
    __tablename__ = "katilimcilar_katilimci"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), unique=True)
    telefon = Column(String(15), nullable=True)
    dogum_tarihi = Column(Date, nullable=True)
    adres = Column(Text, nullable=True)
    sehir = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    profil_resmi = Column(String(255), nullable=True)
    website = Column(String(200), nullable=True)
    linkedin = Column(String(200), nullable=True)
    twitter = Column(String(200), nullable=True)
    email_bildirim = Column(Boolean, default=True)
    sms_bildirim = Column(Boolean, default=False)
    kayit_tarihi = Column(DateTime, default=datetime.now)
    son_guncelleme = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # İlişkiler
    kayitlar = relationship("Kayit", back_populates="katilimci")


class Kayit(Base):
    """
    Kayıt modeli (SQLAlchemy)
    """
    __tablename__ = "kayitlar_kayit"
    
    id = Column(Integer, primary_key=True, index=True)
    katilimci_id = Column(Integer, ForeignKey("katilimcilar_katilimci.id"))
    etkinlik_id = Column(Integer, ForeignKey("etkinlikler_etkinlik.id"))
    durum = Column(String(20), default="beklemede")
    kayit_turu = Column(String(20), default="normal")
    odendi = Column(Boolean, default=False)
    odeme_tarihi = Column(DateTime, nullable=True)
    odeme_yontemi = Column(String(50), nullable=True)
    notlar = Column(Text, nullable=True)
    kayit_tarihi = Column(DateTime, default=datetime.now)
    guncelleme_tarihi = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # İlişkiler
    katilimci = relationship("Katilimci", back_populates="kayitlar")
    etkinlik = relationship("Etkinlik", back_populates="kayitlar")


class Organizator(Base):
    """
    Organizatör modeli (SQLAlchemy)
    """
    __tablename__ = "organizatorler_organizator"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), unique=True)
    telefon = Column(String(15), nullable=True)
    organizasyon_adi = Column(String(100), nullable=True)
    pozisyon = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    adres = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    profil_resmi = Column(String(255), nullable=True)
    linkedin = Column(String(200), nullable=True)
    twitter = Column(String(200), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    kayit_tarihi = Column(DateTime, default=datetime.now)
    son_guncelleme = Column(DateTime, default=datetime.now, onupdate=datetime.now) 