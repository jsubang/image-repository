#!/usr/bin/env python

import MySQLdb
import MySQLdb.cursors


def get_db(psw):
    db = MySQLdb.connect(
        host = "img-repo-db.czwcl89wj6vg.us-east-2.rds.amazonaws.com",
        port = 3306,
        user = "admin",
        passwd = psw,
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
def add_image(user_id, filename, filetype, cursor, db):
    
    # TODO error check if a file already exists in the server...

    insert = "INSERT INTO image (user_id, filename, filetype) VALUES ({0}, '{1}', '{2}')".format(user_id, filename, filetype)
    cursor.execute(insert)
    db.commit()
    return True

def get_image():
    pass

def get_all_images(cursor):
    sel_cmd = "SELECT * FROM image"
    cursor.execute(sel_cmd)
    result = ()    
    result = cursor.fetchall()
    return result

# gets the id number that will correspond to the filename in the uploads directory, returns either a tuple or None
def get_image_id(user_id, filename, cursor):
    user_condition = "user_id = {0}".format(user_id)
    file_condition = "filename = '{0}'".format(filename)
    sel_cmd = "SELECT DISTINCT file_id FROM image WHERE {0} AND {1}".format(user_condition, file_condition)
    cursor.execute(sel_cmd)
    result = () 
    result = cursor.fetchone()
    return result