import sys
import time
import os
from flask import Flask, render_template, redirect, request
from werkzeug.utils import secure_filename
sys.path.insert(0, "db/")
from db.dbhelper import *

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    students = getall('students')
    return render_template('index.html', studentlist=students)

@app.route("/save_student", methods=["POST"])
def save_student():
    data = {
        'idno': request.form['idno'],
        'lastname': request.form['lastname'],
        'firstname': request.form['firstname'],
        'course': request.form['course'],
        'level': request.form['level']
    }

    original_idno = request.form.get('original_idno')
    picture_file = request.files.get('picture')
    captured_image = request.form.get('captured_image')

    # Handle uploaded file
    if picture_file and picture_file.filename != "" and allowed_file(picture_file.filename):
        filename = secure_filename(f"{int(time.time())}_{picture_file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        picture_file.save(filepath)
        data['image'] = filename
    # Handle webcam captured image
    elif captured_image:
        header, encoded = captured_image.split(",", 1)
        filename = f"{int(time.time())}_webcam.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(encoded))
        data['image'] = filename
    else:
        if not original_idno:
            data['image'] = None

    if original_idno:  # update
        updates = data.copy()
        if original_idno == data['idno']:
            updates.pop('idno')
        updaterecord('students', where={'idno': original_idno}, updates=updates)
    else:  # add new
        addrecord('students', **data)

    return redirect("/")



@app.route("/edit_student/<idno>")
def edit_student(idno):
    student = getrecord('students', idno=idno)
    if not student:
        return redirect("/")
    return render_template('index.html', studentlist=getall('students'), edit_student=student[0])

@app.route("/delete_student/<idno>", methods=["POST"])
def delete_student(idno):
    deleterecord('students', idno=idno)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
