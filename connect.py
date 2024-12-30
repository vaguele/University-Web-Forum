import mysql.connector

conn = mysql.connector.connect(  #con stands for connection to database
  host="UCMSocialMediaApp.mysql.pythonanywhere-services.com",
  user="UCMSocialMediaAp",  # last p lost?
  password="mysqlpassword",
  database="UCMSocialMediaAp$default"
)

mycursor = conn.cursor() #cursor object that can execut mysql queries

mycursor.execute("SELECT * FROM loginInfo")

myresult = mycursor.fetchall()  #returns rows

for x in myresult:
  print(x)