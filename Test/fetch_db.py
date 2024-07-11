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

# for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):

for scores in Score.select().order_by(Score.score.desc()):
    print(scores.name, scores.score)
    
#db.close()