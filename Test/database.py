from peewee import *
import pandas as pd  

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

dataNombre = ['Lucas','Stella','Eduardo']
dataScore = [45,67,234]
data = {'Nombre': dataNombre, 'Score': dataScore}
df_global = pd.DataFrame(data)

for index, row in df_global.iterrows():
    lucas = Score(name=row.Nombre, score=row.Score)
    lucas.save()

for scores in Score.select():
    print(scores.name, scores.score)
    
# for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):

db.close()
