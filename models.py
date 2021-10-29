import peewee as pw

db = pw.SqliteDatabase('db.db')
import random, string

class BaseModel(pw.Model):
    class Meta:
        database = db


class Repository(BaseModel):
    code = pw.CharField(unique=True, default=''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(10)]))
    path = pw.CharField()