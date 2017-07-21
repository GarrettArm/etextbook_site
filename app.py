import os
from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/var/www/uploads'
app.config['SECRET_KEY'] = os.urandom(24)

ALLOWED_FILETYPES = set('csv', )

@app.route('/', methods=['GET', 'POST']) 
def clean_up(errors=None):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return render_template('cleanup.html', errors={'errors': ["the file not being specified", ]})
        file = request.files['file']
        if file.filename == '':
            flash('No file')
        if file and allow_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('hello', given_name=filename))

    else:
        return render_template('cleanup.html')


def allow_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_FILETYPES



@app.route('/hello')
@app.route('/hello/<given_name>/')
def name(given_name=None):
    return render_template('hello.html', name=given_name)

@app.route('/do_something/')
def doing():
    print('hello')
    return redirect(url_for('front_page'))
