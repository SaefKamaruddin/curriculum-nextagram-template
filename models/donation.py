from models.base_model import BaseModel
from models.user import User
from models.images import Images
import peewee as pw
from playhouse.hybrid import hybrid_property


class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref="user_donated", null=True)
    image = pw.ForeignKeyField(Images, backref="image_donated", null=True)
    amount = pw. DecimalField(null=False)
    transaction_number = pw.CharField(null=False)
