# Minimal app.py for Vercel
from flask import Flask, request, jsonify
import os
import requests
import pickle
import io

app = Flask(__name__)

def download_model(url):
    try:
        response = requests.get(url)
        return pickle.loads(response.content)
    except Exception as e:
        return None

@app.route('/predict', methods=['POST'])
def predict():
    model_url = os.getenv('https://drive.google.com/file/d/1c81xUHgZOAak5etD5K2WjPqP0RzXL9Xc/view?usp=drive_link')
    model = download_model(model_url)
    
    if not model:
        return jsonify({'error': 'Model load failed'}), 500
    
    question = request.json.get('question', '')
    # Minimal prediction logic
    return jsonify({'answer': 'Sample answer'})
