from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/pages/users',
    tags=['Pages_users']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def user_login(request: Request):
    return templates.TemplateResponse('users/login.html', {"request": request})
