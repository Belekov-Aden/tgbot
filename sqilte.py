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
    '''
    Создание таблицы, в случае если его нету
    :return: table Users; table NameApp
    '''
    if not connect.table_exists([Users, NameApp]):
        connect.create_tables([Users, NameApp])


async def insert_id_users(id_users: int):
    '''
    Добавление id пользователя в БД
    :param id_users: идентификатор пользователя
    :return: создание пользователя в БД
    '''
    if not Users.get_or_none(Users.id_users == id_users):
        Users.create(id_users=id_users)


async def insert_name_password(id: int, name: str, password: str):
    '''
    Занести в БД, имя приложения и парооль
    :param id: id пользователя
    :param name: имя
    :param password: пароль
    :return:
    '''
    if Users.select(Users.id).where(Users.id_users==id).get():
        id_s = Users.select(Users.id).where(Users.id_users==id).get()
        NameApp.create(users=id_s, name=name, password=password)
    else:
        await insert_id_users(id_users=id)


async def get_users_app(id: int):
    '''
    Получение приложение  пользователя
    :param id: идентификатор
    :return: данные из БД
    '''
    idusers = Users.select(Users.id).where(Users.id_users==id).get()
    return NameApp.select(NameApp.name, NameApp.password).where(NameApp.users==idusers)



async def delete_app_from_db(id: int, name: str, password: str) -> None:
    '''
    Получение данных для удаление из БД
    :param id: идентификатор
    :param name: имя
    :param password: пароль
    :return:
    '''
    idusers = Users.select(Users.id).where(Users.id_users == id).get()
    return NameApp.delete().where(NameApp.users==idusers, NameApp.name==name, NameApp.password==password).execute()

