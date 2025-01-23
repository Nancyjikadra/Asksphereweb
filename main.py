from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load the model
with open('model.pkl', 'rb') as f:
    pipeline = pickle.load(f)

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    questions = data.get('questions', [])
    video_paths = data.get('video_paths', [])
    results = pipeline.answer_questions(questions, video_paths)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
