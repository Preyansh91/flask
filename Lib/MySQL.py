import MySQLdb as db
import sys
import re
import os

class SQL(object):

    def __init__(self,*args, **kwargs):
        try:
            self.db_init(*args, **kwargs)
        except db.Error as e:
            print e
            if con:
                con.close()
            return None

    def db_init(self,*args,**kwargs):
        con = db.connect("127.0.0.1", "root", "default", "flask", local_infile = 1)
        self.con = con
        cursor = self.con.cursor()
        cursor.connection.autocommit(True)
        self.cursor = cursor

    def register_user_db(self,*args,**kwargs):
        cur = self.con.cursor()
        if args:
            try:
                cur.execute("""insert into users(username, password, email) values (%s, %s, %s)""", (args[0], args[1], args[2]))
                return True
            except Exception as e:
                print e
                return e
        return False
