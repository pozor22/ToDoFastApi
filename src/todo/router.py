from fastapi import APIRouter, Depends
from todo.schemas import TaskCreate
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_async_session
from todo.models import Task
from user.base_config import current_user
from user.models import User
from sqlalchemy import insert, select, delete, update

router = APIRouter(
    prefix='/task',
    tags=['task']
)


@router.get('/user_task')
async def get_user_tasks(user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.user_id == user.id)
    result = await session.execute(query)
    return {
        'status': 200,
        'data': result.scalars().all(),
        'details': None
    }


@router.post('/new_task')
async def add_new_task(
        new_task: TaskCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    new_task.user_id = user.id
    stmt = insert(Task).values(**new_task.dict())
    result = await session.execute(stmt)
    await session.commit()
    return {
        'status': 200,
        'data': {
            'id': result.inserted_primary_key[0],
            'description': new_task.description,
            'is_done': new_task.is_done,
            'user_id': new_task.user_id
        },
        'details': None
    }


@router.post('/done')
async def done_task(task_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    test = await session.get(Task, task_id)
    if test.user_id == user.id:
        if test.is_done:
            stmt = update(Task).where(Task.id == task_id).values(is_done=False)
            await session.execute(stmt)
            await session.commit()

            return {'status': 'change'}
        else:
            stmt = update(Task).where(Task.id == task_id).values(is_done=True)
            await session.execute(stmt)
            await session.commit()

            return {'status': 'change'}
    return {'status': 'idi naxui'}


@router.delete('/delete_task')
async def delete_task(task_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    task = await session.get(Task, task_id)
    if task.user_id == user.id:
        stmt = delete(Task).where(Task.id == task_id)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 200,
            'data': task,
            'details': 'delete this task'
        }
    return {
        'status': 200,
        'data': None,
        'details': 'you dont have enough rights to delete this task'
    }
