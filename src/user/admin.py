from sqladmin import ModelView
from user.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username,
                   User.is_active, User.is_superuser, User.is_verified, User.is_verified]
