# =============================================================================
# KATILIMCILAR API ROUTER
# =============================================================================
# Bu dosya katılımcılar için API endpoint'lerini tanımlar

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Katilimci])
async def get_katilimcilar(
    skip: int = Query(0, ge=0, description="Atlanacak kayıt sayısı"),
    limit: int = Query(100, ge=1, le=1000, description="Döndürülecek kayıt sayısı"),
    sehir: Optional[str] = Query(None, description="Şehir"),
    email_bildirim: Optional[bool] = Query(None, description="E-posta bildirimleri"),
    db: Session = Depends(get_db)
):
    """
    Tüm katılımcıları listele
    
    - **skip**: Atlanacak kayıt sayısı (sayfalama için)
    - **limit**: Döndürülecek kayıt sayısı (maksimum 1000)
    - **sehir**: Belirli bir şehre göre filtrele
    - **email_bildirim**: E-posta bildirim tercihine göre filtrele
    """
    query = db.query(models.Katilimci)
    
    if sehir:
        query = query.filter(models.Katilimci.sehir == sehir)
    
    if email_bildirim is not None:
        query = query.filter(models.Katilimci.email_bildirim == email_bildirim)
    
    katilimcilar = query.offset(skip).limit(limit).all()
    return katilimcilar


@router.get("/{katilimci_id}", response_model=schemas.Katilimci)
async def get_katilimci(katilimci_id: int, db: Session = Depends(get_db)):
    """
    Belirli bir katılımcıyı getir
    
    - **katilimci_id**: Katılımcı ID'si
    """
    katilimci = db.query(models.Katilimci).filter(models.Katilimci.id == katilimci_id).first()
    if katilimci is None:
        raise HTTPException(status_code=404, detail="Katılımcı bulunamadı")
    return katilimci


@router.post("/", response_model=schemas.Katilimci)
async def create_katilimci(katilimci: schemas.KatilimciCreate, db: Session = Depends(get_db)):
    """
    Yeni katılımcı oluştur
    
    - **katilimci**: Katılımcı bilgileri
    """
    # Aynı kullanıcı için birden fazla katılımcı profili oluşturulmasını engelle
    existing_katilimci = db.query(models.Katilimci).filter(
        models.Katilimci.user_id == katilimci.user_id
    ).first()
    
    if existing_katilimci:
        raise HTTPException(status_code=400, detail="Bu kullanıcı için zaten katılımcı profili var")
    
    db_katilimci = models.Katilimci(**katilimci.dict())
    db.add(db_katilimci)
    db.commit()
    db.refresh(db_katilimci)
    return db_katilimci


@router.put("/{katilimci_id}", response_model=schemas.Katilimci)
async def update_katilimci(
    katilimci_id: int, 
    katilimci: schemas.KatilimciUpdate, 
    db: Session = Depends(get_db)
):
    """
    Katılımcı güncelle
    
    - **katilimci_id**: Katılımcı ID'si
    - **katilimci**: Güncellenecek katılımcı bilgileri
    """
    db_katilimci = db.query(models.Katilimci).filter(models.Katilimci.id == katilimci_id).first()
    if db_katilimci is None:
        raise HTTPException(status_code=404, detail="Katılımcı bulunamadı")
    
    update_data = katilimci.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_katilimci, field, value)
    
    db.commit()
    db.refresh(db_katilimci)
    return db_katilimci


@router.delete("/{katilimci_id}", response_model=schemas.Message)
async def delete_katilimci(katilimci_id: int, db: Session = Depends(get_db)):
    """
    Katılımcı sil
    
    - **katilimci_id**: Katılımcı ID'si
    """
    db_katilimci = db.query(models.Katilimci).filter(models.Katilimci.id == katilimci_id).first()
    if db_katilimci is None:
        raise HTTPException(status_code=404, detail="Katılımcı bulunamadı")
    
    db.delete(db_katilimci)
    db.commit()
    return {"message": "Katılımcı başarıyla silindi", "success": True}


@router.get("/sehir/{sehir}", response_model=List[schemas.Katilimci])
async def get_sehir_katilimcilari(
    sehir: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Belirli bir şehirdeki katılımcıları listele
    
    - **sehir**: Şehir adı
    """
    katilimcilar = db.query(models.Katilimci).filter(
        models.Katilimci.sehir == sehir
    ).offset(skip).limit(limit).all()
    return katilimcilar


@router.get("/user/{user_id}", response_model=schemas.Katilimci)
async def get_user_katilimci(user_id: int, db: Session = Depends(get_db)):
    """
    Kullanıcı ID'sine göre katılımcıyı getir
    
    - **user_id**: Kullanıcı ID'si
    """
    katilimci = db.query(models.Katilimci).filter(models.Katilimci.user_id == user_id).first()
    if katilimci is None:
        raise HTTPException(status_code=404, detail="Katılımcı bulunamadı")
    return katilimci


@router.put("/{katilimci_id}/bildirimler", response_model=schemas.Katilimci)
async def update_katilimci_bildirimler(
    katilimci_id: int,
    email_bildirim: bool,
    sms_bildirim: bool,
    db: Session = Depends(get_db)
):
    """
    Katılımcının bildirim tercihlerini güncelle
    
    - **katilimci_id**: Katılımcı ID'si
    - **email_bildirim**: E-posta bildirimleri
    - **sms_bildirim**: SMS bildirimleri
    """
    db_katilimci = db.query(models.Katilimci).filter(models.Katilimci.id == katilimci_id).first()
    if db_katilimci is None:
        raise HTTPException(status_code=404, detail="Katılımcı bulunamadı")
    
    db_katilimci.email_bildirim = email_bildirim
    db_katilimci.sms_bildirim = sms_bildirim
    db.commit()
    db.refresh(db_katilimci)
    return db_katilimci 