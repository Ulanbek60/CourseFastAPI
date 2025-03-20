from fastapi import Depends, HTTPException, APIRouter
from course_app.db.database import SessionLocal
from starlette.requests import Request
from course_app.config import settings
from authlib.integrations.starlette_client import OAuth


oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize',
)
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_KEY,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)


social_auth_router = APIRouter(prefix='/social_auth', tags=['Social_Auth'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@social_auth_router.get('/github')
async def github_login(request: Request):
    redirect_url = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_url)


@social_auth_router.get('/google')
async def google_login(request: Request):
    redirect_url = settings.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request, redirect_url)
