from peewee import *

# Define your database connection
db = SqliteDatabase('scores.db')

class Score(Model):
    name = CharField()
    score = IntegerField()

    class Meta:
        database = db

# Create the table if it doesn't exist
db.connect()
db.create_tables([Score])
