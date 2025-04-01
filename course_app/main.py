import fastapi
from course_app.db.database import engine
import uvicorn
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from sqladmin import Admin
from course_app.admin.setup import setup_admin
from course_app.api.endpoints import (about, answer, assignment, auth_teacher, auth_student, category, certificate, course,
                                      exam, lesson, option, questions, social_auth, student, teacher, teacher_review, cart, favorite)
from starlette.middleware.sessions import SessionMiddleware
from course_app.config import SECRET_KEY
from fastapi_pagination import add_pagination


async def init_redis():
    return redis.Redis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


course_app = fastapi.FastAPI(title='Course', lifespan=lifespan)
course_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

admin = Admin(course_app, engine)


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
setup_admin(course_app)
add_pagination(course_app)

course_app.include_router(auth_teacher.auth_teacher_router)
course_app.include_router(auth_student.auth_student_router)
course_app.include_router(category.category_router)
course_app.include_router(about.about_router)
course_app.include_router(answer.answer_router)
course_app.include_router(assignment.assignment_router)
course_app.include_router(certificate.certificate_router)
course_app.include_router(course.course_router)
course_app.include_router(exam.exam_router)
course_app.include_router(lesson.lesson_router)
course_app.include_router(option.option_router)
course_app.include_router(questions.questions_router)
course_app.include_router(social_auth.social_auth_router)
course_app.include_router(student.student_router)
course_app.include_router(teacher.teacher_router)
course_app.include_router(teacher_review.teacher_review_router)
course_app.include_router(cart.cart_router)
course_app.include_router(favorite.favorite_router)


if __name__ == "__main__":
    uvicorn.run(course_app, host="127.0.0.1", port=8001)
