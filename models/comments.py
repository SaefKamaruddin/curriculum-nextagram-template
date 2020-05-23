from models.base_model import BaseModel
from models.user import User
from models.images import Images
import peewee as pw
from playhouse.hybrid import hybrid_property


class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref="user_commented", null=True)
    image = pw.ForeignKeyField(Images, backref="image_commented", null=True)
    comment = pw.TextField(null=False)
    deleted = pw.BooleanField(null=False, default=False)
