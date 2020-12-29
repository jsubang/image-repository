#!/usr/bin/env python

import os
import json

from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

# database functions
from database import *

def get_files():

    records = []

    for x in get_all_images():

        if (x[4] == 1 and x[1] != session['user_id']):
            continue
        else:
            records.append({
                'file_id':x[0],
                'user_id':x[1],
                'filename':x[2].split('.')[0],
                'private':x[4],
                'filetype':x[5]
            })
    
    return json.dumps(records)


UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__, static_url_path='')
app.secret_key = 'gXL0cmGE6vwUxmhYOnzxXEuHNq1e6u2zGUDLni1v'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

# logout
def logout():
    session['logged_in'] = False
    session['username'] = ""
    session['user_id'] = -1
    return

# deletes the image file from the server
def delete_image_file(file_id):

    filetype = get_image_type(file_id)
    filename = UPLOAD_FOLDER + str(file_id) + '.' + filetype

    # check if the file exists
    if (os.path.exists(filename)):
        os.remove(filename)
    else:
        print(filename + " not deleted because the file was not found.")
    return

# get the database credentials
# db = get_db(name)
# cursor = db.cursor()

# close db
# cursor.close()
# db.close()

@app.route('/')
def index(name=None):

    print("ok")


    return render_template('index.html', name=name)


@app.route('/login', methods=['post'])
def login(name=None):

    login_details = request.get_json()
    username = login_details[0]["value"]
    password = login_details[1]["value"]
    response = []
    db_password = get_user_password(username)


    # if its blank, username did not exist, return 
    if(db_password == ""):
        response.append({"message":"username does not exist"})
        return json.dumps(response), 404

    # check if password is valid
    if(db_password == password):
        response.append({"message":"Correct password"})
        session['logged_in'] = True
        session['username'] = username
        session['user_id'] = get_user_id(username)
        return json.dumps(response), 200

    else:
        response.append({"message":"Incorrect password"})
        return json.dumps(response), 401

@app.route('/logout', methods = ['post'])
def logout_request(name = None):
    logout()
    return redirect(url_for('index')), 200

# get public images only
@app.route('/get_images', methods=['get'])
def get_images(name=None):
    return get_files(), 200


@app.route('/del_image', methods=['DELETE'])
def delete(name=None):

    if(session['logged_in'] == False):
        return "user not logged in", 401

    to_del = request.get_json()
    
    # get the file_id and file type
    file_id = to_del["file_id"]

    # get the current logged in user.
    owner = get_image_owner(file_id)

    if (owner == -1):
        return "image does not exist", 404
    
    if (owner == session['user_id']):
       
        # remove the file from the server
        delete_image_file(file_id)

        # remove from database
        del_image_record(file_id)


        return "file deleted", 200

    else:
        return "user does not own the file", 401

@app.route('/multiupload', methods=['post'])
def multiupload(name=None):

    # cursor = db.cursor()

    img = request.files['file']

    private_file = request.form['private']
    private_setting = -1
    if (private_file == 'true'):
        private_setting = 1
    else:
        private_setting = 0


    filename = secure_filename(img.filename)
    file_type = '.' + filename.split('.')[1]


    image_id = get_image_id(session['user_id'], filename)
    if (image_id != -1):
        delete_image_file(image_id)
        del_image_record(image_id)   

    add_image(6, filename, filename.split('.')[1], private_setting)

    # get the generated file_id from the server
    output = get_image_id(6, filename)

    if (output != -1):
        file_id = get_image_id(6, filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], str(file_id) + file_type))
    
    return "image uploaded", 200


# @app.route('/upload', methods=['post'])
# def upload(name=None):

#     img = request.files['file']
#     filename = secure_filename(img.filename)
#     file_type = '.' + filename.split('.')[1]

#     # create a new image file record in the database
#     # TODO allow private and public, will need to change add_image

#     # TODO error check if a file already exists in the server...
#     # allow overwrite, so delete record and create new one
#     # allow to specify public private


#     add_image(6, filename, filename.split('.')[1])

#     # # get the generated file_id from the server
#     # output = get_image_id(6, filename)

#     # if (output != ()):
#     #     file_id = get_image_id(6, filename)
#     #     img.save(os.path.join(app.config['UPLOAD_FOLDER'], str(file_id) + file_type))

#     # else:
#     #     pass
#     #     # TODO error handle

#     # return redirect(url_for('index'))

# # get list of uploaded items from the server, put it a JSON, return JSON to frontend for it to create the pictures 