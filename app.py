from flask import Flask, request, render_template
import os
from model import VideoQAPipeline

# Load the pipeline model
def load_model():
    """Initialize the VideoQAPipeline model."""
    try:
        model = VideoQAPipeline()  # Initialize directly
        print("Model initialized successfully!")
        return model
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        raise

# Flask app setup
app = Flask(__name__)

# Initialize the model
model = load_model()

@app.route('/')
def home():
    """Home route."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get the question from the form
        question = request.form['question']
        print(f"Question received: {question}")

        # Define video paths (update these paths as per your setup)
        video_paths = [
            "C:/Users/HP/trialrender/videoplayback (2).mp4",  # Replace with your actual video paths
            "C:/Users/HP/trialrender/videoplayback.mp4"
        ]

        # Get the model's response
        responses = model.answer_questions([question], video_paths)
        answer = responses[question]['answer']
        confidence = responses[question]['confidence']

        print(f"Answer generated: {answer} (Confidence: {confidence})")

        # Render the result on the web page
        return render_template(
            'index.html',
            prediction_text=f'Answer: {answer} (Confidence: {confidence:.2f})'
        )
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

@app.route('/health')
def health():
    """Health check route."""
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
