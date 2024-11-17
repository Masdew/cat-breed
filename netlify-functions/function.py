from flask import Flask, jsonify
from flask_lambda import FlaskLambda

# Membuat aplikasi Flask
app = FlaskLambda(__name__)

# Mendefinisikan endpoint yang mengembalikan JSON
@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask on Netlify!"})

# Fungsi handler untuk Netlify
def handler(event, context):
    # Netlify Function menghubungkan Flask ke request dan response
    return app(event, context)
