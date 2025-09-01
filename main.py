# =============================================================================
# ETKİNLİK YÖNETİMİ - FASTAPI ANA DOSYASI
# =============================================================================
# Bu dosya FastAPI sunucusunu başlatır ve API endpoint'lerini tanımlar
# Django ile birlikte çalışarak REST API hizmeti sağlar

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

# API modüllerini import et
from api.database import engine, get_db
from api import models, schemas
from api.routers import etkinlikler, kayitlar, katilimcilar

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Etkinlik Yönetimi API",
    description="Etkinlik yönetimi sistemi için REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS ayarları (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Production'da spesifik domain'ler belirtin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# API router'larını ekle
app.include_router(etkinlikler.router, prefix="/api/v1/etkinlikler", tags=["Etkinlikler"])
app.include_router(kayitlar.router, prefix="/api/v1/kayitlar", tags=["Kayıtlar"])
app.include_router(katilimcilar.router, prefix="/api/v1/katilimcilar", tags=["Katılımcılar"])


@app.get("/")
async def root():
    """
    Ana endpoint - API hakkında bilgi verir
    """
    return {
        "message": "Etkinlik Yönetimi API'ye Hoş Geldiniz!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/v1/health")
async def health_check():
    """
    Sağlık kontrolü endpoint'i
    
    Bu endpoint API'nin çalışıp çalışmadığını kontrol eder
    """
    return {
        "status": "healthy",
        "message": "API çalışıyor"
    }


@app.get("/api/v1/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    İstatistik endpoint'i
    
    Bu endpoint sistem genelindeki istatistikleri döndürür
    """
    try:
        # Etkinlik sayısı
        etkinlik_sayisi = db.query(models.Etkinlik).count()
        
        # Katılımcı sayısı
        katilimci_sayisi = db.query(models.Katilimci).count()
        
        # Kayıt sayısı
        kayit_sayisi = db.query(models.Kayit).count()
        
        # Onaylı kayıt sayısı
        onayli_kayit_sayisi = db.query(models.Kayit).filter(
            models.Kayit.durum == 'onaylandi'
        ).count()
        
        return {
            "etkinlik_sayisi": etkinlik_sayisi,
            "katilimci_sayisi": katilimci_sayisi,
            "kayit_sayisi": kayit_sayisi,
            "onayli_kayit_sayisi": onayli_kayit_sayisi
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"İstatistik alınırken hata: {str(e)}")


if __name__ == "__main__":
    """
    FastAPI sunucusunu başlat
    
    Bu kısım dosya doğrudan çalıştırıldığında çalışır
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # Geliştirme modu - kod değişikliklerinde otomatik yeniden başlat
        log_level="info"
    ) 