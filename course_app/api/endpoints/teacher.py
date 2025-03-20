from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Teacher
from course_app.db.schema import TeacherSchema
from course_app.db.database import SessionLocal
from typing import List

teacher_router = APIRouter(prefix='/teacher', tags=['Teacher'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@teacher_router.post('/', response_model=TeacherSchema)
async def teacher_create(teacher: TeacherSchema, db: Session = Depends(get_db)):
    teacher_db = Teacher(**teacher.dict())
    db.add(teacher_db)
    db.commit()
    db.refresh(teacher_db)
    return teacher_db


@teacher_router.get('/', response_model=List[TeacherSchema])
async def teacher_list(db: Session = Depends(get_db)):
    return db.query(Teacher).all()


@teacher_router.get('/{teacher_id}/', response_model=TeacherSchema)
async def teacher_detail(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail='Преподаватель не найден')
    return teacher


@teacher_router.put('/{teacher_id}/', response_model=TeacherSchema)
async def teacher_update(teacher_id: int, teacher: TeacherSchema, db: Session = Depends(get_db)):
    teacher_db = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher_db is None:
        raise HTTPException(status_code=404, detail='Преподаватель не найден')

    for key, value in teacher.dict().items():
        setattr(teacher_db, key, value)

    db.add(teacher_db)
    db.commit()
    db.refresh(teacher_db)
    return teacher_db


@teacher_router.delete('/{teacher_id}/')
async def teacher_delete(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail='Преподаватель не найден')

    db.delete(teacher)
    db.commit()
    return {"message": "Преподаватель удалён"}
