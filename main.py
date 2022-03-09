import os
from app import app
import urllib.request
import uuid
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
def pencilsketch(filename,pencilfilename):
    image = cv2.imread(filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = 255 - gray_image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    cv2.imwrite(pencilfilename, pencil_sketch)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        generated_filename = os.path.join("static/generated_art/",str(uuid.uuid4()) + filename[3:])
        print(generated_filename)
        filename2=generated_filename
        inputfile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Making pencil sketch, source\toutput\n{inputfile}\t{filename2}")
        pencilsketch(inputfile,filename2)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        return render_template('upload.html', filename=filename,filename2=filename2)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):

    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



if __name__ == "__main__":
    app.run(debug=True)
