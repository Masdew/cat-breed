from flask import Flask, request, render_template, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import os  # Import os untuk environment variables

app = Flask(__name__)

# Load model menggunakan path dari environment variables
model_path = os.getenv('MODEL_PATH', 'modelbaru1.h5')  # Default ke 'modelbaru1.h5'
model = load_model(model_path)

# Map label ke prediksi
label_map = {0: 'Angora', 1: 'Persian', 2: 'Ragdoll', 3: 'Bengal'}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
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
        return render_template('result.html', predicted_label=predicted_label)
    
    # Jika method GET, tampilkan halaman prediksi
    return render_template('predict.html')

@app.route('/artikel1')
def artikel1():
    return render_template('artikel1.html')

@app.route('/artikel2')
def artikel2():
    return render_template('artikel2.html')

@app.route('/artikel3')
def artikel3(): 
    return render_template('artikel3.html')

# Route untuk halaman feedback
@app.route('/notsure', methods=['GET', 'POST'])
def feedback():
    return render_template('notsure.html')

if __name__ == '__main__':
    app.run(debug=True)
