from fastapi import APIRouter, Depends
from todo.schemas import TaskCreate
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_async_session
from todo.models import Task
from sqlalchemy import insert

router = APIRouter(
    prefix='/task',
    tags=['task']
)


@router.post('/new_task')
async def add_new_task(new_task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Task).values(**new_task.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
