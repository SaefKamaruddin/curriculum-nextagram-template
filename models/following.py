from models.base_model import BaseModel
from models.user import User
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin, current_user, login_user, logout_user


class Following(BaseModel):
    # refers to the User that is being followed
    idol = pw.ForeignKeyField(User)

    # refers to the User that is following another user
    fan = pw.ForeignKeyField(User)

    # when a fan wants to follow an idol, it is automatically true;
    # UNLESS user has set their is_private to true; hence it will automatically be set to false
    # idol will have to manually approve  to set to true
    approved = pw.BooleanField(null=False, default=True)

    block = pw.BooleanField(null=False, default=False)

    def validate(self):
        if self.fan_id == self.idol_id:
            self.errors.append("Cannot follow self")
