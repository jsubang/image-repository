import os
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index(name=None):

    return render_template('index.html', name=name)


@app.route('/upload', methods=['post'])
def upload(name=None):

    img = request.files['file']

    filename = secure_filename(img.filename)
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("file {0} has been uploaded".format(filename))
    return redirect(url_for('index'))