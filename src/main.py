from fastapi import FastAPI
from user.base_config import auth_backend, fastapi_users
from user.schemas import UserRead, UserCreate
from sqladmin import Admin
from settings.database import engine
from user.admin import UserAdmin
from todo.admin import TaskAdmin
from todo.router import router as router_todo

app = FastAPI()
admin = Admin(app, engine)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_todo)

admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
