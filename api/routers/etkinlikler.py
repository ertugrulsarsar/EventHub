# =============================================================================
# ETKİNLİKLER API ROUTER
# =============================================================================
# Bu dosya etkinlikler için API endpoint'lerini tanımlar

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Etkinlik])
async def get_etkinlikler(
    skip: int = Query(0, ge=0, description="Atlanacak kayıt sayısı"),
    limit: int = Query(100, ge=1, le=1000, description="Döndürülecek kayıt sayısı"),
    kategori_id: Optional[int] = Query(None, description="Kategori ID'si"),
    durum: Optional[str] = Query(None, description="Etkinlik durumu"),
    db: Session = Depends(get_db)
):
    """
    Tüm etkinlikleri listele
    
    - **skip**: Atlanacak kayıt sayısı (sayfalama için)
    - **limit**: Döndürülecek kayıt sayısı (maksimum 1000)
    - **kategori_id**: Belirli bir kategoriye göre filtrele
    - **durum**: Belirli bir duruma göre filtrele
    """
    query = db.query(models.Etkinlik)
    
    if kategori_id:
        query = query.filter(models.Etkinlik.kategori_id == kategori_id)
    
    if durum:
        query = query.filter(models.Etkinlik.durum == durum)
    
    etkinlikler = query.offset(skip).limit(limit).all()
    return etkinlikler


@router.get("/{etkinlik_id}", response_model=schemas.Etkinlik)
async def get_etkinlik(etkinlik_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir etkinliği getir
    
    - **etkinlik_id**: Etkinlik ID'si
    """
    etkinlik = db.query(models.Etkinlik).filter(models.Etkinlik.id == etkinlik_id).first()
    if etkinlik is None:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    return etkinlik


@router.post("/", response_model=schemas.Etkinlik)
async def create_etkinlik(etkinlik: schemas.EtkinlikCreate, db: Session = Depends(get_db)):
    """
    Yeni etkinlik oluştur
    
    - **etkinlik**: Etkinlik bilgileri
    """
    db_etkinlik = models.Etkinlik(**etkinlik.dict())
    db.add(db_etkinlik)
    db.commit()
    db.refresh(db_etkinlik)
    return db_etkinlik


@router.put("/{etkinlik_id}", response_model=schemas.Etkinlik)
async def update_etkinlik(
    etkinlik_id: int, 
    etkinlik: schemas.EtkinlikUpdate, 
    db: Session = Depends(get_db)
):
    """
    Etkinlik güncelle
    
    - **etkinlik_id**: Etkinlik ID'si
    - **etkinlik**: Güncellenecek etkinlik bilgileri
    """
    db_etkinlik = db.query(models.Etkinlik).filter(models.Etkinlik.id == etkinlik_id).first()
    if db_etkinlik is None:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    update_data = etkinlik.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_etkinlik, field, value)
    
    db.commit()
    db.refresh(db_etkinlik)
    return db_etkinlik


@router.delete("/{etkinlik_id}", response_model=schemas.Message)
async def delete_etkinlik(etkinlik_id: int, db: Session = Depends(get_db)):
    """
    Etkinlik sil
    
    - **etkinlik_id**: Etkinlik ID'si
    """
    db_etkinlik = db.query(models.Etkinlik).filter(models.Etkinlik.id == etkinlik_id).first()
    if db_etkinlik is None:
        raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")
    
    db.delete(db_etkinlik)
    db.commit()
    return {"message": "Etkinlik başarıyla silindi", "success": True}


@router.get("/kategori/{kategori_id}", response_model=List[schemas.Etkinlik])
async def get_kategori_etkinlikleri(
    kategori_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Belirli bir kategorideki etkinlikleri listele
    
    - **kategori_id**: Kategori ID'si
    """
    etkinlikler = db.query(models.Etkinlik).filter(
        models.Etkinlik.kategori_id == kategori_id
    ).offset(skip).limit(limit).all()
    return etkinlikler


@router.get("/durum/{durum}", response_model=List[schemas.Etkinlik])
async def get_durum_etkinlikleri(
    durum: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Belirli bir durumdaki etkinlikleri listele
    
    - **durum**: Etkinlik durumu (planlandi, aktif, tamamlandi, iptal)
    """
    etkinlikler = db.query(models.Etkinlik).filter(
        models.Etkinlik.durum == durum
    ).offset(skip).limit(limit).all()
    return etkinlikler 