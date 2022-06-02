import peewee
from peewee import *
from .config import config
import psycopg2

db_handle = PostgresqlDatabase(
    config.get("db_name"),
    user=config.get("user_name"),
    password=config.get("password"),
    host=config.get("host"),
    port=config.get("port")
)


class BaseModel(Model):
    class Meta:
        database = db_handle


class Ratings(BaseModel):
    name = CharField(unique=True)
    accuracy = IntegerField(null=False)
    WPM = IntegerField(null=False)

    class Meta:
        db_table = "ratings"


def init_connection():
    db_handle.connect()


def create_row(user):
    row = dict(zip(['name', 'accuracy', 'WPM', 'mistakes'], [v for v in str(user).split(', ')]))
    row['accuracy'] = float(row.get('accuracy'))
    row['WPM'] = float(row.get('WPM'))
    Ratings.insert(row).execute()


def insert(user):
    try:
        Ratings.create_table()
        create_row(user)
    except peewee.InternalError as px:
        print(str(px))


def show_top():
    rows = Ratings.select().order_by(-Ratings.WPM)
    for i in range(5 % len(rows)):
        return f"{i + 1})  ID: {rows[i]}\tName: {rows[i].name} {rows[i].wpm}"


def show_result(name: str):
    row = Ratings.select().where(Ratings.name == name)
    for i in row:
        return f"ID:{i}\tName: {i.name}\tWPM: {i.WPM}\taccuracy: {i.accuracy}"
