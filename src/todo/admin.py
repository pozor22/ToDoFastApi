from sqladmin import ModelView
from todo.models import Task


class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.name, Task.description, Task.is_done, Task.user_id]
