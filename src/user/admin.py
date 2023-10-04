from sqladmin import ModelView
from user.models import User


class UserAdmin(ModelView, model=User):
    column_list = '__all__'
