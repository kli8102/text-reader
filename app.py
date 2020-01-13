import os
from flask import Flask, flash, redirect, url_for, request, render_template, \
send_from_directory, safe_join
from werkzeug.utils import secure_filename
import ocr as reader

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')

@app.route('/stats', methods=['GET', 'POST'])
def render_stats():
    if request.method == 'POST':
        result = request.form
        return render_template('stats.html', result = result)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                
                return render_template('index.html')

            if allowed_file(image.filename):
                text = reader.ocr_core(image)


                return render_template('index.html', result = text, img = image.filename)
            else:
                print("This file extension is not allowed")
                return redirect(request.url)

    return render_template('index.html')

@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(os.path.join(APP_ROOT, 'images/'), filename)


        # if 'file' not in result:
        #     flash('No file part')
        #     return redirect()
        # file = request.files['file']
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect()
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     file.save(path)
        #     text = reader.ocr_core(path)
        #     return render_template('index.html', text = text)

        # return redirect()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
