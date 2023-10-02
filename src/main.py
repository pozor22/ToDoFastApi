from fastapi import FastAPI
from user.base_config import auth_backend, fastapi_users
from user.schemas import UserRead, UserCreate

app = FastAPI()

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
