from models.base_model import BaseModel
from models.user import User
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin, current_user, login_user, logout_user


class Following(BaseModel):
    # refers to the User that is following another user
    user = pw.ForeignKeyField(User, backref="Follower")
    # refers to the User that is being followed
    followed = pw.ForeignKeyField(User, backref="Followed")

    def validate(self):
        if self.user_id == self.follower_id:
            self.errors.append("Cannot follow self")
