#!/usr/bin/env python

import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# database functions
from database import *

UPLOAD_FOLDER = 'static/uploads/'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, static_url_path='')
app.secret_key = 'gXL0cmGE6vwUxmhYOnzxXEuHNq1e6u2zGUDLni1v'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

db = get_db()
cursor = db.cursor()


@app.route('/')
def index(name=None):

    # add_user("miles", "pass", cursor, db)

    # del_user('user_id', 1, cursor, db)

    # print(get_user('username', 'miles', cursor))

    # edit user
    # edit_user('username', 'miles', 6, cursor, db)

    print(add_user('dude', 'oookkk', cursor, db))

    return render_template('index.html', name=name)


@app.route('/upload', methods=['post'])
def upload(name=None):

    img = request.files['file']

    filename = secure_filename(img.filename)
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("file {0} has been uploaded".format(filename))
    return redirect(url_for('index'))