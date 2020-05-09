
from models.base_model import BaseModel
from models.user import User
import peewee as pw


class Follow(BaseModel):
    user = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    approved = pw.BooleanField(default=False)

    def validate(self):
        if self.user_id == self.follower_id:
            self.errors.append('You cannot follow yourself')
