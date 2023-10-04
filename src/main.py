from fastapi import FastAPI, Depends
from user.base_config import auth_backend, fastapi_users
from user.schemas import UserRead, UserCreate
from sqladmin import Admin
from settings.database import engine
from user.admin import UserAdmin
from todo.admin import TaskAdmin
from todo.router import router as router_todo
from user.models import User
from user.base_config import current_user

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


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
