from sqladmin import ModelView
from todo.models import Task


class TaskAdmin(ModelView, model=Task):
    column_list = '__all__'
