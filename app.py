#!/usr/bin/env python

import os
import json

from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

# database functions
from database import *

psw = "jarrylsubang"

def get_files(cursor):
    # print(type(get_all_images(cursor)))

    records = []

    for x in get_all_images(cursor):

        records.append({
            'file_id':x[0],
            'user_id':x[1],
            'filename':x[2].split('.')[0],
            # 'upload_date':x[3], raw swl data is not serializable when using json.dumps()
            'private':x[4],
            'filetype':x[5]
        })

        
    # print(records)
    return json.dumps(records)


UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__, static_url_path='')
app.secret_key = 'gXL0cmGE6vwUxmhYOnzxXEuHNq1e6u2zGUDLni1v'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"


db = get_db(psw)
cursor = db.cursor()

# debug
def debug():
    session['logged_in'] = False
    session['username'] = "Miles"
    session['user_id'] = 6
    return



@app.route('/')
def index(name=None):

    # print(add_user('dude', 'oookkk', cursor, db))
    debug()
    # session get the user_id when someone logs in...
    # also get the username so the webpage will say welcome

    return render_template('index.html', name=name)


@app.route('/login', methods=['post'])
def login(name=None):
    login_details = request.get_json()
    return redirect(url_for('index'))


@app.route('/get_images', methods=['get'])
def get_images(name=None):
    # get_files(cursor)
    return get_files(cursor)

@app.route('/del_image', methods=['DELETE'])
def delete(name=None):
    to_del = request.get_json()
    
    # id is to_del["file_id"]
    print(to_del["file_id"])

    # get the current logged in user.



    return "hueheuhue"



@app.route('/upload', methods=['post'])
def upload(name=None):

    img = request.files['file']
    filename = secure_filename(img.filename)
    file_type = '.' + filename.split('.')[1]
    add_image(6, filename, filename.split('.')[1], cursor, db)

    # gets the generated file_id from the server which will be used to rename the 
    # newly uploaded image.
    output = get_image_id(6, filename, cursor)
    if (output != ()):
        file_id = get_image_id(6, filename, cursor)[0]
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], str(file_id) + file_type))

    else:
        pass
        # TODO error handle

    return redirect(url_for('index'))

# get list of uploaded items from the server, put it a JSON, return JSON to frontend for it to create the pictures 