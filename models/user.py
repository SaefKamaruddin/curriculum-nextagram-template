from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
import re
from flask_login import UserMixin, current_user, login_user, logout_user

# REGEX for password


def has_lower(word):
    return re.search("[a-z]", word)


def has_upper(word):
    return re.search("[A-Z]", word)


def has_special(word):
    return re.search("[\W]", word)


class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null=False)
    profile_image = pw.CharField(null=True)
    is_private = pw.BooleanField(null=False, default=False)
    about_me = pw.TextField(null=True)

    # adds the aws url to the image file
    @hybrid_property
    def profile_image_url(self):
        from app import app
        if self.profile_image == None:
            return "#"
        else:
            return app.config.get('AWS_DOMAIN') + self.profile_image

    # tracks the fans a particular user has
    @hybrid_property
    def fans(self):
        from models.following import Following
        return User.select().join(Following, on=(User.id == Following.fan_id)).where(Following.idol_id == self.id)

    # tracks the number of user a particular user is following; how many user is a particular user a fan of
    @hybrid_property
    def following(self):
        from models.following import Following
        return User.select.join(Following, on=(User.id == Following.fan_id)).where(Following.fan_id == self.id)

    # parameters that user data has to fulfill upon data creation
    # if all parameters fulfilled, password is hashed before being entered into database
    def validate(self):
        existing_email = User.get_or_none(email=self.email)
        existing_username = User.get_or_none(username=self.username)

        if existing_email != None:
            self.errors.append("User's email already exists")

        if existing_username != None:
            self.errors.append("Username already taken")

        if len(self.password) < 6:
            self.errors.append(
                "Password needs to be a minimum of 6 characters")

        if not has_lower(self.password):
            self.errors.append(
                "Passwords needs at least one lowercase character")

        if not has_upper(self.password):
            self.errors.append(
                "Passwords needs at least one uppercase character")

        if not has_special(self.password):
            self.errors.append(
                "Passwords needs at least one special character")

        else:
            self.password = generate_password_hash(self.password)
