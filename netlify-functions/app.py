from flask import Flask, request, jsonify, render_template
from flask_lambda import FlaskLambda
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import os

# Membuat aplikasi Flask
app = FlaskLambda(__name__)

# Load model menggunakan path dari environment variables
model_path = os.getenv('MODEL_PATH', 'modelbaru1.h5')  # Default ke 'modelbaru1.h5'
model = load_model(model_path)

# Map label ke prediksi
label_map = {0: 'Angora', 1: 'Persian', 2: 'Ragdoll', 3: 'Bengal'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image = None

    # Memproses gambar dari unggahan file
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        image = Image.open(file.stream)  # Memuat gambar dari stream file
    elif 'url' in request.form and request.form['url'] != '':
        # Mengambil gambar dari URL
        image_url = request.form['url']
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            return f"Error loading image from URL: {str(e)}"

    if image is None:
        return "No image provided. Please upload an image file or provide a URL."

    # Memproses gambar dan mempersiapkannya untuk prediksi
    image = image.resize((256, 256))  # Ubah ukuran gambar sesuai model
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0  # Normalisasi gambar

    # Melakukan prediksi
    predictions = model.predict(image)
    predicted_label = label_map[np.argmax(predictions)]

    # Kirim hasil prediksi ke template result.html
    return jsonify(predicted_label=predicted_label)

# Fungsi handler untuk Netlify
def handler(event, context):
    # Netlify Function menghubungkan Flask ke request dan response
    return app(event, context)

