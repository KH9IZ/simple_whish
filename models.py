from peewee import CharField, Model, BigIntegerField
from playhouse.pool import PooledSqliteDatabase

db = PooledSqliteDatabase(
    '/var/db/simple_whish/simple_whish.db',
    max_connections=2,
    check_same_thread=False,
)


class BaseModel(Model):
    class Meta:
        database = db


class Whish(BaseModel):
    uid = BigIntegerField()
    title = CharField()
    description = CharField(null=True)


def create_tables():
    db.connect()
    db.create_tables([Whish])
    db.close()


def connect_db():
    db.connect()


def close_db():
    if not db.is_closed():
        db.close()
