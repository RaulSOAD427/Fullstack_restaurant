# Add the necessary imports
import mysql.connector as mysql
import os
import datetime

from dotenv import load_dotenv
load_dotenv("credentials.env")
# Read Database connection variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']


# Connect to the db and create a cursor object
db =mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE if not exists TechAssignment6")
cursor.execute("USE TechAssignment6")

try:
	cursor.execute("""
	CREATE TABLE Menu_Items (
		 item_id          integer  AUTO_INCREMENT PRIMARY KEY,
		 name        VARCHAR(100) NOT NULL,  
		 price       int
	);
 """)
except RuntimeError as err:
	print("runtime error: {0}".format(err))


try:
	cursor.execute("""
	CREATE TABLE Orders (
		 order_id          integer  AUTO_INCREMENT PRIMARY KEY,
		 item_id          int,
		 name        VARCHAR(100) NOT NULL,  
		 quantity       int,
		 status          int
	);
 """)
except RuntimeError as err:
	print("runtime error: {0}".format(err))

