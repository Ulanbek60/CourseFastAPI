from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Certificate
from course_app.db.schema import CertificateSchema
from course_app.db.database import SessionLocal
from typing import List

certificate_router = APIRouter(prefix='/certificate', tags=['Certificate'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@certificate_router.post('/', response_model=CertificateSchema)
async def certificate_create(certificate: CertificateSchema, db: Session = Depends(get_db)):
    certificate_db = Certificate(**certificate.dict())
    db.add(certificate_db)
    db.commit()
    db.refresh(certificate_db)
    return certificate_db


@certificate_router.get('/', response_model=List[CertificateSchema])
async def certificate_list(db: Session = Depends(get_db)):
    return db.query(Certificate).all()


@certificate_router.get('/{certificate_id}/', response_model=CertificateSchema)
async def certificate_detail(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Сертификат не найден')
    return certificate


@certificate_router.put('/{certificate_id}/', response_model=CertificateSchema)
async def certificate_update(certificate_id: int, certificate: CertificateSchema, db: Session = Depends(get_db)):
    certificate_db = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate_db is None:
        raise HTTPException(status_code=404, detail='Сертификат не найден')

    for key, value in certificate.dict().items():
        setattr(certificate_db, key, value)

    db.add(certificate_db)
    db.commit()
    db.refresh(certificate_db)
    return certificate_db


@certificate_router.delete('/{certificate_id}/')
async def certificate_delete(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.query(Certificate).filter(Certificate.id == certificate_id).first()
    if certificate is None:
        raise HTTPException(status_code=404, detail='Сертификат не найден')

    db.delete(certificate)
    db.commit()
    return {"message": "Сертификат удалён"}
