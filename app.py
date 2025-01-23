from flask import Flask, request, render_template, jsonify
from model_loader import download_model_from_drive
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Google Drive shareable link for model
DRIVE_MODEL_LINK = os.getenv('DRIVE_MODEL_LINK')

# Load model globally
try:
    model = download_model_from_drive(DRIVE_MODEL_LINK)
except Exception as e:
    logger.error(f"Model loading failed: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        question = request.form.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Define video paths (use cloud storage links)
        video_paths = [
            os.getenv('VIDEO_PATH_1', 'default_video_path'),
            os.getenv('VIDEO_PATH_2', 'default_video_path')
        ]

        # Process question
        responses = model.answer_questions([question], video_paths)
        result = responses[question]

        return jsonify({
            'answer': result['answer'],
            'confidence': result['confidence']
        })

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

# Vercel requires this for serverless deployment
if __name__ == "__main__":
    app.run()
