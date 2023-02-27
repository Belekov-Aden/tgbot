import asyncio
import peewee
from config import PGUSER,PGPASSWORD, HOST

connect = peewee.PostgresqlDatabase(
    'tguser',
    user=PGUSER,
    password=PGPASSWORD,
    host=HOST
)


class BaseModel(peewee.Model):
    id = peewee.PrimaryKeyField(unique=True)
    class Meta:
        database = connect
        order_by = 'id'


class Users(BaseModel):
    id_users = peewee.BigIntegerField()
    class Meta:
        db_table = 'Users'


class NameApp(BaseModel):
    users = peewee.ForeignKeyField(Users, db_column='users_id')
    name = peewee.CharField(max_length=30)
    password = peewee.CharField(max_length=15)
    class Meta:
        db_table = 'Name_app'



async def create_table():
    if not connect.table_exists([Users, NameApp]):
        connect.create_tables([Users, NameApp])


async def insert_id_users(id_users: int):
    if not Users.get_or_none(Users.id_users == id_users):
        Users.create(id_users=id_users)


async def insert_name_password(id: int, name: str, password: str):
    if Users.select(Users.id).where(Users.id_users==id).get():
        id_s = Users.select(Users.id).where(Users.id_users==id).get()
        NameApp.create(users=id_s, name=name, password=password)
    else:
        await insert_id_users(id_users=id)


async def get_users_app(id: int):
    idusers = Users.select(Users.id).where(Users.id_users==id).get()
    return NameApp.select(NameApp.name, NameApp.password).where(NameApp.users==idusers)



async def delete_app_from_db(id: int, name: str, password: str) -> None:
    idusers = Users.select(Users.id).where(Users.id_users == id).get()
    return NameApp.delete().where(NameApp.users==idusers, NameApp.name==name, NameApp.password==password).execute()

