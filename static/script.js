// Fungsi untuk memuat model TensorFlow.js
async function loadModel() {
    const model = await tf.loadLayersModel('static/tfjs_model/model.json');
    console.log('Model Loaded!');
    return model;
}

// Fungsi untuk membaca dan menampilkan gambar yang diunggah
function readImage(file) {
    const reader = new FileReader();
    reader.onload = function (event) {
        const imgElement = document.getElementById('image-preview');
        imgElement.src = event.target.result;
        imgElement.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Fungsi untuk memproses gambar dan melakukan prediksi
async function predict(image, model) {
    // Memuat dan mengolah gambar menjadi tensor
    const img = new Image();
    img.src = URL.createObjectURL(image);
    img.onload = async () => {
        const tensor = tf.browser.fromPixels(img)
            .resizeNearestNeighbor([256, 256])  // Sesuaikan ukuran dengan input model
            .toFloat()
            .div(tf.scalar(255.0))
            .expandDims();

        // Melakukan prediksi
        const predictions = await model.predict(tensor).data();

        // Mendapatkan prediksi label dengan probabilitas tertinggi
        const labels = ['Angora', 'Persian', 'Ragdoll'];
        const predictedLabel = labels[predictions.indexOf(Math.max(...predictions))];

        // Menampilkan hasil prediksi
        document.getElementById('prediction').innerText = `Prediksi: ${predictedLabel}`;
    };
}

// Memuat model dan menyiapkan event listener untuk file input
window.onload = async () => {
    const model = await loadModel();
    const fileInput = document.getElementById('image-upload');

    // Event listener untuk file upload
    fileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            readImage(file);  // Menampilkan gambar yang diunggah
            await predict(file, model);  // Melakukan prediksi pada gambar
        }
    });
};
