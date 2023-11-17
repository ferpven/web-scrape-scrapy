import mysql.connector
from getpass import getpass
import json

db = mysql.connector.connect(
    host="localhost",
    user=input("Enter username: "),
    password=getpass("Enter password: "),
    database="petlebi",
)

with open("petlebi_products.json") as json_file:
    data = json.load(json_file)

cursor = db.cursor()

columns = ", ".join(data[0].keys())
placeholder = ", ".join(["%s"] * len(data[0]))

count = 0
for i in range(len(data)):
    sql = "INSERT INTO petlebi ( %s ) VALUES ( %s )" % (columns, placeholder)
    cursor.execute(sql, list(data[i].values()))
    count += 1
    db.commit()

print(count, "record inserted")
