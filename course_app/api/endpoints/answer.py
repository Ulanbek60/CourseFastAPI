from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import AnswerStudent
from course_app.db.schema import AnswerStudentSchema
from course_app.db.database import SessionLocal
from typing import List

answer_router = APIRouter(prefix='/answer', tags=['AnswerStudent'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@answer_router.post('/', response_model=AnswerStudentSchema)
async def answer_create(answer: AnswerStudentSchema, db: Session = Depends(get_db)):
    answer_db = AnswerStudent(**answer.dict())
    db.add(answer_db)
    db.commit()
    db.refresh(answer_db)
    return answer_db


@answer_router.get('/', response_model=List[AnswerStudentSchema])
async def answer_list(db: Session = Depends(get_db)):
    return db.query(AnswerStudent).all()


@answer_router.get('/{answer_id}/', response_model=AnswerStudentSchema)
async def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(AnswerStudent).filter(AnswerStudent.id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail='Ответ не найден')
    return answer


@answer_router.put('/{answer_id}/', response_model=AnswerStudentSchema)
async def answer_update(answer_id: int, answer: AnswerStudentSchema, db: Session = Depends(get_db)):
    answer_db = db.query(AnswerStudent).filter(AnswerStudent.id == answer_id).first()
    if answer_db is None:
        raise HTTPException(status_code=404, detail='Ответ не найден')

    for key, value in answer.dict().items():
        setattr(answer_db, key, value)

    db.add(answer_db)
    db.commit()
    db.refresh(answer_db)
    return answer_db


@answer_router.delete('/{answer_id}/')
async def answer_delete(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(AnswerStudent).filter(AnswerStudent.id == answer_id).first()
    if answer is None:
        raise HTTPException(status_code=404, detail='Ответ не найден')

    db.delete(answer)
    db.commit()
    return {"message": "Ответ удалён"}
