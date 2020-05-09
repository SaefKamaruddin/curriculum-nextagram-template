from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
import os


class Images (BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    img = pw.CharField()

    @hybrid_property
    def img_url(self):
        from app import app
        return app.config.get('AWS_DOMAIN') + self.img
