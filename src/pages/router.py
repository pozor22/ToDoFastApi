from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from todo.router import get_user_tasks

router = APIRouter(prefix='/pages', tags=['Pages'])

templates = Jinja2Templates(directory='templates')


@router.get('/')
def list_tasks(request: Request, tasks=Depends(get_user_tasks)):
    context = {
        'request': request,
        'tasks': tasks['data'],
    }
    return templates.TemplateResponse('tasks/tasks.html', context)
