from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Questions
from course_app.db.schema import QuestionsSchema
from course_app.db.database import SessionLocal
from typing import List

questions_router = APIRouter(prefix='/questions', tags=['Questions'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@questions_router.post('/', response_model=QuestionsSchema)
async def question_create(question: QuestionsSchema, db: Session = Depends(get_db)):
    question_db = Questions(**question.dict())
    db.add(question_db)
    db.commit()
    db.refresh(question_db)
    return question_db


@questions_router.get('/', response_model=List[QuestionsSchema])
async def question_list(db: Session = Depends(get_db)):
    return db.query(Questions).all()


@questions_router.get('/{question_id}/', response_model=QuestionsSchema)
async def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Questions).filter(Questions.id == question_id).first()

    if question is None:
        raise HTTPException(status_code=404, detail='Вопрос не найден')
    return question


@questions_router.put('/{question_id}/', response_model=QuestionsSchema)
async def question_update(question_id: int, question: QuestionsSchema, db: Session = Depends(get_db)):
    question_db = db.query(Questions).filter(Questions.id == question_id).first()

    if question_db is None:
        raise HTTPException(status_code=404, detail='Вопрос не найден')
    for key, value in question.dict().items():
        setattr(question_db, key, value)

    db.add(question_db)
    db.commit()
    db.refresh(question_db)
    return question_db


@questions_router.delete('/{question_id}/')
async def question_delete(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Questions).filter(Questions.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail='Вопрос не найден')

    db.delete(question)
    db.commit()
    return {"message": "Вопрос удалён"}
