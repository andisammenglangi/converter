from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')

    image_list = []
    for f in files:
        img = Image.open(f)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        image_list.append(img)

    pdf_bytes = io.BytesIO()
    image_list[0].save(pdf_bytes, format='PDF', save_all=True, append_images=image_list[1:])
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name='result.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
