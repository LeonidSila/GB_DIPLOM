import sqlite3


conn = None
cursor = None
def creat_teble():
    global conn
    global cursor
    conn = sqlite3.connect('user_db.sql')
    cursor = conn.cursor()
    
