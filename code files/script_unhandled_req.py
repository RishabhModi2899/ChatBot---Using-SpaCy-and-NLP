#This is a script that contains functions to make entries in the Database of unhandled requests

#imports
import sqlite3
from sqlite3 import Error

#Functions to create the database in sqlite3 for unhandled requests 
def db_unhandled_requests():
  ''' This is a function to create a database for storing the request response pairs that aren't handled by the Chatbot '''
  con = None 
  try :
    #creating the database for the unhandled requests
    con = sqlite3.connect('/Users/rishabh_2/Documents/python projects/chatbot/chatbot ver 5/data base files/Unhandled_requests.db')
    return con
  except Error as e:
    print(e)
  return con

def gen_table_unhandled_requests(connection_obj):
  ''' This is a function that creates a table with the tag , request and response field in the database '''
  #creating the sqlite cursor
  cursor_obj = connection_obj.cursor()
  #creating the table in the database
  cursor_obj.execute("CREATE TABLE IF NOT EXISTS unhandled_request(tag text , request text , response text )")
  #commiting the changes
  connection_obj.commit()

def create_table_entry(connection_obj , user_input , tags_svo = "NULL" , resp = 'NULL'):
  ''' This is a function that makes entries in the table in the database '''
  #creating a entry in the database table
  cursor1 = connection_obj.cursor()
  #inserting the values in the table created 
  cursor1.execute("INSERT INTO unhandled_request(tag , request , response) VALUES(? , ? , ?)" ,[tags_svo , user_input , resp])
  #committing changes 
  connection_obj.commit()
