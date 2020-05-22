from models.base_model import BaseModel
from models.user import User
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin, current_user, login_user, logout_user

# REGEX for password


class Images(BaseModel, UserMixin):
    user = pw.ForeignKeyField(User, backref="user_images", null=True)
    image = pw.CharField(null=False)

    @hybrid_property
    def image_url(self):
        from app import app
        if self.image == None:
            return "#"
        else:
            return app.config.get('AWS_DOMAIN') + self.image
