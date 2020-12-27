#!/usr/bin/env python

import MySQLdb
import MySQLdb.cursors


def get_db():
    db = MySQLdb.connect(
        host = "img-repo-db.czwcl89wj6vg.us-east-2.rds.amazonaws.com",
        port = 3306,
        user = "admin",
        passwd = "IfoRGot1t",
        db = "testdb")
    return db

##### General db functions #####

# Deletes an entry from a table
def del_record(column, value, cursor, db, table):

    del_cmd = "DELETE FROM {0} WHERE {1} = '{2}'".format(table, column, value)
    cursor.execute(del_cmd)
    db.commit()
    return

# Gets a user from the database if it exists, Returns None if user is not found 
def get_record(column, value, cursor, table):

    sel_cmd = "SELECT * FROM {0} WHERE {1} = '{2}'".format(table, column, value)
    cursor.execute(sel_cmd)
    result = None    
    result = cursor.fetchone()
    return result


###### functions for user table #####

# Adds a user to the database, returns True if successful, False if the add failed
def add_user(username, password, cursor, db):

    # if username exists, cancel
    if (get_record('username', username, cursor, 'user') != None):
        return False

    insert = "INSERT INTO user (username, password) VALUES (%s, %s)"
    values = (username, password)
    cursor.execute(insert, values)
    db.commit()
    return True

# Edits a attribute for a user
def edit_user(col, value, user_id, cursor, db):
    edit_cmd = "UPDATE user SET {0} = '{1}' WHERE user_id = '{2}'".format(col, value, user_id)
    cursor.execute(edit_cmd)
    db.commit()
    return


##### functions for image table #####


