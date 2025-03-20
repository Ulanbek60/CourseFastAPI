from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from course_app.db.models import Assignment
from course_app.db.schema import AssignmentSchema
from course_app.db.database import SessionLocal
from typing import List

assignment_router = APIRouter(prefix='/assignment', tags=['Assignment'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@assignment_router.post('/')
async def assignment_create(assignment: AssignmentSchema, db: Session = Depends(get_db)):
    assignment_db = Assignment(**assignment.dict())
    db.add(assignment_db)
    db.commit()
    db.refresh(assignment_db)
    return assignment_db


@assignment_router.get('/', response_model=List[AssignmentSchema])
async def assignment_list(db: Session = Depends(get_db)):
    return db.query(Assignment).all()


@assignment_router.get('/{assignment_id}/', response_model=AssignmentSchema)
async def assignment_detail(assignment_id: int,db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment is None:
        raise  HTTPException(status_code=400, detail='Мындай маалымат жок')
    return assignment


@assignment_router.put('/{assignment_id}', response_model=AssignmentSchema)
async def assignment_update(assignment_id: int, assignment: AssignmentSchema, db: Session = Depends(get_db)):
    assignment_db = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment_db is None:
        raise HTTPException(status_code=404, detail='такого задания не существует')

    # Применяем данные из Pydantic-схемы к объекту SQLAlchemy
    for key, value in assignment.dict().items():
        setattr(assignment_db, key, value)

    db.commit()
    db.refresh(assignment_db)
    return assignment_db


@assignment_router.delete('/{assignment_id}')
async def assignment_delete(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id==assignment_id).first()
    if assignment is None:
        raise HTTPException(status_code=404, detail='такого задание не существует')

    db.delete(assignment)
    db.commit()
    return {"message": 'This assignment deleted'}


