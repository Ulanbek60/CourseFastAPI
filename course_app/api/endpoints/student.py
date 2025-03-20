from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Student
from course_app.db.schema import StudentSchema
from course_app.db.database import SessionLocal
from typing import List

student_router = APIRouter(prefix='/student', tags=['Student'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@student_router.post('/', response_model=StudentSchema)
async def student_create(student: StudentSchema, db: Session = Depends(get_db)):
    student_db = Student(**student.dict())
    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return student_db


@student_router.get('/', response_model=List[StudentSchema])
async def student_list(db: Session = Depends(get_db)):
    return db.query(Student).all()


@student_router.get('/{student_id}/', response_model=StudentSchema)
async def student_detail(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail='Студент не найден')
    return student


@student_router.put('/{student_id}/', response_model=StudentSchema)
async def student_update(student_id: int, student: StudentSchema, db: Session = Depends(get_db)):
    student_db = db.query(Student).filter(Student.id == student_id).first()
    if student_db is None:
        raise HTTPException(status_code=404, detail='Студент не найден')

    for key, value in student.dict().items():
        setattr(student_db, key, value)

    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return student_db


@student_router.delete('/{student_id}/')
async def student_delete(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail='Студент не найден')

    db.delete(student)
    db.commit()
    return {"message": "Студент удалён"}
