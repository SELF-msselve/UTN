import mysql.connector
import pandas as pd

# Connect to the database
mydb = mysql.connector.connect(
  host="mysql-179d8e-self-01.a.aivencloud.com",
  user="avnadmin",
  password="AVNS_crGnD2-St8ZyJ5xX0sS",
  database="stor_db"
)

# Create a cursor object
my_cursor = mydb.cursor()

# Execute the query to fetch all data from the table
my_cursor.execute("SELECT * FROM customers")

# Fetch all the results
results = my_cursor.fetchall()

# Get column names from the description attribute
column_names = [i[0] for i in my_cursor.description]

# Create a pandas DataFrame
df = pd.DataFrame(results, columns=column_names)

# Close the connection
mydb.close()

# Print the DataFrame
print(df)