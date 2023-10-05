from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from todo.router import get_user_tasks
from todo.models import Task
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_async_session
from user.base_config import current_user
from user.models import User
from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse
from todo.router import delete_task, done_task


router = APIRouter(prefix='/pages/todo', tags=['Pages_todo'])

templates = Jinja2Templates(directory='templates')


@router.get('/')
def list_tasks(request: Request,
               tasks=Depends(get_user_tasks)):
    context = {
        'request': request,
        'tasks': tasks['data'],
    }
    return templates.TemplateResponse('tasks/tasks.html', context)


@router.get('/done/{task_id}')
async def task_done(task=Depends(done_task)):
    url = router.url_path_for('list_tasks')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@router.get('/delete/{task_id}')
async def delete_task(task_delete=Depends(delete_task)):
    url = router.url_path_for('list_tasks')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@router.post('/post_new_task')
async def post_new_task(Name: str = Form(...),
                        Description: str = Form(...),
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)
                        ):
    new_todo = Task(name=Name, description=Description, is_done=False, user_id=user.id)

    session.add(new_todo)
    await session.commit()

    url = router.url_path_for('list_tasks')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
