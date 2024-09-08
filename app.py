from flask import Flask, render_template, request, send_file
import pytesseract
import cv2
import os

app = Flask(__name__)

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Ensure the upload directory exists
upload_dir = 'static/uploads'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        # Process image and extract text
        image = cv2.imread(file_path)
        extracted_text = pytesseract.image_to_string(image)

        # Save extracted text to a file
        text_file_path = os.path.join(upload_dir, file.filename + '.txt')
        with open(text_file_path, 'w') as f:
            f.write(extracted_text)

        return render_template('result.html', image_filename=file.filename, extracted_text=extracted_text)

@app.route('/download')
def download_text():
    filename = request.args.get('filename')
    if filename:
        text_file_path = os.path.join(upload_dir, filename + '.txt')
        if os.path.exists(text_file_path):
            return send_file(text_file_path, as_attachment=True)

    return 'File not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
