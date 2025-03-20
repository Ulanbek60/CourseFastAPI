from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Option
from course_app.db.schema import OptionSchema
from course_app.db.database import SessionLocal
from typing import List

option_router = APIRouter(prefix='/option', tags=['Option'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@option_router.post('/', response_model=OptionSchema)
async def option_create(option: OptionSchema, db: Session = Depends(get_db)):
    option_db = Option(**option.dict())
    db.add(option_db)
    db.commit()
    db.refresh(option_db)
    return option_db


@option_router.get('/', response_model=List[OptionSchema])
async def option_list(db: Session = Depends(get_db)):
    return db.query(Option).all()


@option_router.get('/{option_id}/', response_model=OptionSchema)
async def option_detail(option_id: int, db: Session = Depends(get_db)):
    option = db.query(Option).filter(Option.id == option_id).first()
    if option is None:
        raise HTTPException(status_code=404, detail='Опция не найдена')
    return option


@option_router.put('/{option_id}/', response_model=OptionSchema)
async def option_update(option_id: int, option: OptionSchema, db: Session = Depends(get_db)):
    option_db = db.query(Option).filter(Option.id == option_id).first()
    if option_db is None:
        raise HTTPException(status_code=404, detail='Опция не найдена')

    for key, value in option.dict().items():
        setattr(option_db, key, value)

    db.add(option_db)
    db.commit()
    db.refresh(option_db)
    return option_db


@option_router.delete('/{option_id}/')
async def option_delete(option_id: int, db: Session = Depends(get_db)):
    option = db.query(Option).filter(Option.id == option_id).first()
    if option is None:
        raise HTTPException(status_code=404, detail='Опция не найдена')

    db.delete(option)
    db.commit()
    return {"message": "Опция удалена"}
