from peewee import SqliteDatabase, Model, TextField, IntegerField

db = SqliteDatabase("posts.db")

class BaseTable(Model):
    class Meta:
        database = db

class Posts(BaseTable):
    id = IntegerField(null=False, primary_key=True, index=True)
    userId = IntegerField(null=False)
    title= TextField(null=False)
    body= TextField(null=False)

