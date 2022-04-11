import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Bar7drori!",
  database="mydatabase"
)
print(mydb)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE mydatabase")
mycursor.execute("CREATE TABLE images (imageUrl VARCHAR(255), scrapeTime TIMESTAMP , keyword VARCHAR(255))")