from fastapi import APIRouter, Depends
from todo.schemas import TaskCreate
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_async_session
from todo.models import Task
from sqlalchemy import insert, select, delete
from user.base_config import current_user
from user.models import User

router = APIRouter(
    prefix='/task',
    tags=['task']
)


@router.post('/new_task')
async def add_new_task(
        new_task: TaskCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    new_task.user_id = user.id
    stmt = insert(Task).values(**new_task.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


@router.get('/user_task')
async def get_user_tasks(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.user_id == user.id)
    result = await session.execute(query)
    return {
        'data': result.scalars().all(),
    }


@router.get('/delete_task')
async def delete_task(task_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    test = await session.get(Task, task_id)
    if test.user_id == user.id:
        stmt = delete(Task).where(Task.id == task_id)
        await session.execute(stmt)
        await session.commit()

        return {'status': 'norm'}
    return {'status': 'idi naxui'}
