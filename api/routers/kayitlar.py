# =============================================================================
# KAYITLAR API ROUTER
# =============================================================================
# Bu dosya kayıtlar için API endpoint'lerini tanımlar

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Kayit])
async def get_kayitlar(
    skip: int = Query(0, ge=0, description="Atlanacak kayıt sayısı"),
    limit: int = Query(100, ge=1, le=1000, description="Döndürülecek kayıt sayısı"),
    durum: Optional[str] = Query(None, description="Kayıt durumu"),
    katilimci_id: Optional[int] = Query(None, description="Katılımcı ID'si"),
    etkinlik_id: Optional[int] = Query(None, description="Etkinlik ID'si"),
    db: Session = Depends(get_db)
):
    """
    Tüm kayıtları listele
    
    - **skip**: Atlanacak kayıt sayısı (sayfalama için)
    - **limit**: Döndürülecek kayıt sayısı (maksimum 1000)
    - **durum**: Belirli bir duruma göre filtrele
    - **katilimci_id**: Belirli bir katılımcıya göre filtrele
    - **etkinlik_id**: Belirli bir etkinliğe göre filtrele
    """
    query = db.query(models.Kayit)
    
    if durum:
        query = query.filter(models.Kayit.durum == durum)
    
    if katilimci_id:
        query = query.filter(models.Kayit.katilimci_id == katilimci_id)
    
    if etkinlik_id:
        query = query.filter(models.Kayit.etkinlik_id == etkinlik_id)
    
    kayitlar = query.offset(skip).limit(limit).all()
    return kayitlar


@router.get("/{kayit_id}", response_model=schemas.Kayit)
async def get_kayit(kayit_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir kaydı getir
    
    - **kayit_id**: Kayıt ID'si
    """
    kayit = db.query(models.Kayit).filter(models.Kayit.id == kayit_id).first()
    if kayit is None:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    return kayit


@router.post("/", response_model=schemas.Kayit)
async def create_kayit(kayit: schemas.KayitCreate, db: Session = Depends(get_db)):
    """
    Yeni kayıt oluştur
    
    - **kayit**: Kayıt bilgileri
    """
    # Aynı kişinin aynı etkinliğe birden fazla kayıt olmasını engelle
    existing_kayit = db.query(models.Kayit).filter(
        models.Kayit.katilimci_id == kayit.katilimci_id,
        models.Kayit.etkinlik_id == kayit.etkinlik_id
    ).first()
    
    if existing_kayit:
        raise HTTPException(status_code=400, detail="Bu etkinliğe zaten kayıtlısınız")
    
    db_kayit = models.Kayit(**kayit.dict())
    db.add(db_kayit)
    db.commit()
    db.refresh(db_kayit)
    return db_kayit


@router.put("/{kayit_id}", response_model=schemas.Kayit)
async def update_kayit(
    kayit_id: int, 
    kayit: schemas.KayitUpdate, 
    db: Session = Depends(get_db)
):
    """
    Kayıt güncelle
    
    - **kayit_id**: Kayıt ID'si
    - **kayit**: Güncellenecek kayıt bilgileri
    """
    db_kayit = db.query(models.Kayit).filter(models.Kayit.id == kayit_id).first()
    if db_kayit is None:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    update_data = kayit.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_kayit, field, value)
    
    db.commit()
    db.refresh(db_kayit)
    return db_kayit


@router.delete("/{kayit_id}", response_model=schemas.Message)
async def delete_kayit(kayit_id: int, db: Session = Depends(get_db)):
    """
    Kayıt sil
    
    - **kayit_id**: Kayıt ID'si
    """
    db_kayit = db.query(models.Kayit).filter(models.Kayit.id == kayit_id).first()
    if db_kayit is None:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    db.delete(db_kayit)
    db.commit()
    return {"message": "Kayıt başarıyla silindi", "success": True}


@router.get("/katilimci/{katilimci_id}", response_model=List[schemas.Kayit])
async def get_katilimci_kayitlari(
    katilimci_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Belirli bir katılımcının kayıtlarını listele
    
    - **katilimci_id**: Katılımcı ID'si
    """
    kayitlar = db.query(models.Kayit).filter(
        models.Kayit.katilimci_id == katilimci_id
    ).offset(skip).limit(limit).all()
    return kayitlar


@router.get("/etkinlik/{etkinlik_id}", response_model=List[schemas.Kayit])
async def get_etkinlik_kayitlari(
    etkinlik_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Belirli bir etkinliğin kayıtlarını listele
    
    - **etkinlik_id**: Etkinlik ID'si
    """
    kayitlar = db.query(models.Kayit).filter(
        models.Kayit.etkinlik_id == etkinlik_id
    ).offset(skip).limit(limit).all()
    return kayitlar


@router.put("/{kayit_id}/durum", response_model=schemas.Kayit)
async def update_kayit_durum(
    kayit_id: int,
    durum: str,
    db: Session = Depends(get_db)
):
    """
    Kayıt durumunu güncelle
    
    - **kayit_id**: Kayıt ID'si
    - **durum**: Yeni durum
    """
    db_kayit = db.query(models.Kayit).filter(models.Kayit.id == kayit_id).first()
    if db_kayit is None:
        raise HTTPException(status_code=404, detail="Kayıt bulunamadı")
    
    db_kayit.durum = durum
    db.commit()
    db.refresh(db_kayit)
    return db_kayit 