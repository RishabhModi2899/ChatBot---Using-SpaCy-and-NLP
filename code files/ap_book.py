#This script contains fumctions related to appointment booking 
import sqlite3
from sqlite3 import Error

#functions to make entries in the database if an appointment is to be made 
def appointment(ctr):
    ''' This is a function that will be called when someone wants to book an appointment '''
    ''' CTR is a boolean varialble'''
    print("Bot : Allright! Just mention a few details , please!")
    fname = input("Bot : Please enter your first name - ")
    lname = input("Bot : Please enter your last name - ")
    email = input("Bot : Please enter your email address - ")
    phnum = input("Bot : Please enter your mobile/contact details - ")
    time = input("Bot : Please enter the time suitable to you for the appointment - ")
    date = input("Bot : Please enter the date of the appointment -")
    purp = input("Bot : What will this meet be in regard to ? - ")
    return [fname , lname , email , phnum , date , time , purp] 

#function to make a connection to the database
def database_connection():
    #return the connection object
    con = None
    try:
        con = sqlite3.connect("C:/Users/rishabh_2/Documents/python projects/chatbot/chatbot ver 5/data base files/New-DATABASE-APPOINTMENTS.db")
        return con
    except Error as e: 
        print(e)
    return con 

#function to create the table in the database
def table_create(con):
    #creating the sqlite cursor
    cursor_obj = con.cursor()
    #creating the table in the database 
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS appointments(firstname text , lastname text , mobilenumber int , email text , time text , date text , purpose text)")
    #commiting the changes 
    con.commit()

#function to create the insert the values in the table 
def table_entry(con , entities):
    #creating a new cursor to add the entries in the table created
    cursor_obj1 = con.cursor()
    #inserting the values in the table created
    cursor_obj1.execute('INSERT INTO appointments(firstname , lastname , mobilenumber , email , time , date , purpose) VALUES(? , ? , ? , ? , ? , ? , ?)' , entities)
    #committing changes 
    con.commit()
