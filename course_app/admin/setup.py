from fastapi import FastAPI
from sqladmin import Admin
from .views import *
from course_app.db.database import engine

def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(StudentAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(CategoryAdmin)