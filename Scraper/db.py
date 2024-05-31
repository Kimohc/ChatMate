import json
import mysql.connector

# Load data from the JSON file
with open('profiles.json', 'r') as f:
    data = json.load(f)

# Establish a connection to your MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='chatmate',
    port='3308'
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Insert data into the MySQL database
for item in data:
    # Concatenate photo URLs into a single string separated by a delimiter

    # Assuming you have a table called 'dieren' with columns 'naam', 'geboortedatum', and 'foto'
    sql = "INSERT INTO bots (bot_id, bot_naam, bot_oud , bot_foto, bot_land, bot_geslacht, bot_beschrijving) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (item['bot_id'], item['bot_naam'], item['bot_oud'], item['bot_foto'], item['bot_land'], item['bot_geslacht'], item['bot_beschrijving'])
    cursor.execute(sql, values)

# Commit the changes to the database
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
