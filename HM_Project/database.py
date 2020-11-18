import psycopg2
from flask_restful import Resource
from flask import jsonify
import psycopg2.extensions
import json
from random import randint


class DataBase(Resource):

 

 def insertCustomerData(self,args):
     first_name = args['first_name']
     last_name = args['last_name']
     password = args['password']
     user_name = args['user_name']
     email = args['email']
     phone_no = args['phone_no']
     address = args['address']
     country = args['country']
     postal_code = args['postal_code']
     unique_id = self.generaterandomNumber()
     query = """INSERT INTO db_registration (first_name,last_name,user_name,password,email,phone_no,address,country,postal_code,unique_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id """
     insertdata = (first_name,last_name,user_name,password,email,phone_no,address,country,postal_code,unique_id)
     insertval = self.insertQuery(query,insertdata)
     status = {"status": "1", "id": insertval}
     return jsonify(status)

 def checkCount(self,table,where):
     conn = self.checkConnection()
     cursor = conn.cursor()
     query = "select count(*) from "+ table + " where "+ where
     print(query)
     #query = "select count(*) from db_registration where email = 'joefreeda.30@gmail.com'"
     #cursor.execute(query,(inputdata,))
     cursor.execute(query)
     insertvalue = cursor.fetchone()[0]
     cursor.close()
     conn.commit()
     conn.close()
     return insertvalue

 def generaterandomNumber(self):
     return randint(100, 999)

 def insertQuery(self,query,insertdata):
     conn = self.checkConnection()
     cursor = conn.cursor()
     cursor.execute(query,insertdata)
     insertvalue = cursor.fetchone()[0]
     cursor.close()
     conn.commit()
     conn.close()
     return insertvalue
  

 def checkConnection(self):
     conn = psycopg2.connect(database = "postgres",
                                  user = "postgre",
                                  password = "postgresql",
                                  host = "db-hotel-management.c6i7hzivudlm.us-east-2.rds.amazonaws.com",
                                  port = "5432"
                                  )
     return conn

 def table_exists(dbcon, tablename):
    exists = False
    try:
       dbcur = dbcon.cursor()
       dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
       if dbcur.fetchone()[0] == 1:
        exists = True
        dbcur.close()
        return False
       dbcur.close()
       return True
    except psycopg2.Error as e:
        print (e)
        return exists
 


 @classmethod
 def CreateTable(self):
 
  try:
    connection = psycopg2.connect(database = "postgres",
                                  user = "postgre",
                                  password = "postgresql",
                                  host = "db-hotel-management.c6i7hzivudlm.us-east-2.rds.amazonaws.com",
                                  port = "5432"
                                  )

    cur = connection.cursor()

    if(self.table_exists(connection,"db_registration")):
   
     cur.execute('''CREATE TABLE db_registration
      (ID SERIAL PRIMARY KEY,
      first_name     TEXT     NOT NULL,
      last_name      TEXT     NOT NULL,
      user_name      TEXT     NOT NULL,
      password       TEXT     NOT NULL,
      email          TEXT     NOT NULL,
      phone_no       TEXT     NOT NULL,
      address        TEXT     NOT NULL,
      country        TEXT     NOT NULL,
      postal_code    TEXT     NOT NULL,
      unique_id      TEXT     NOT NULL);''')

    if(self.table_exists(connection,"db_currency")):
     cur.execute('''CREATE TABLE db_currency
      (ID INT PRIMARY KEY     NOT NULL,
      type      TEXT     NOT NULL);''')
   
    if(self.table_exists(connection,"db_location")):
     cur.execute('''CREATE TABLE db_location
      (ID INT PRIMARY KEY     NOT NULL,
      location      TEXT     NOT NULL);''')

    if(self.table_exists(connection,"db_room")):
     cur.execute('''CREATE TABLE db_room
      (ID INT PRIMARY KEY     NOT NULL,
      room_type      TEXT     NOT NULL);''')

    if(self.table_exists(connection,"db_price")):
      cur.execute('''CREATE TABLE db_price
      (ID INT PRIMARY KEY     NOT NULL,
      room_type      INT REFERENCES db_room(ID),
      price          TEXT    NOT NULL);''')

    if(self.table_exists(connection,"db_roombooking")):
      cur.execute('''CREATE TABLE db_roombooking
      (ID INT PRIMARY KEY     NOT NULL,
      unique_id      TEXT     NOT NULL,
      adults         INT     NOT NULL,
      children       INT     NOT NULL,
      rooms          INT     NOT NULL,
      check_in       DATE     NOT NULL,
      check_out      DATE     NOT NULL,
      days           INT     NOT NULL,
      location       INT REFERENCES db_location(ID),
      room_type      INT REFERENCES db_room(ID),
      price_rate     INT REFERENCES db_price(ID));''')


    connection.commit()
    cur.close()
    connection.close()


  except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
  finally:
    #closing database connection.
        if(connection):
           cur.close()
           connection.close()
           print("PostgreSQL connection is closed")

