import os
import json
import numpy as np
import torch
import whisper
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pydub import AudioSegment
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set FFmpeg path manually
AudioSegment.converter = r"C:\ffmpeg\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\ffmpeg-2025-02-02-git-957eb2323a-full_build\bin\ffmpeg.exe"

app = Flask(__name__)
CORS(app)

import psycopg2
from psycopg2.extras import RealDictCursor

# PostgreSQL Connection
DATABASE_URL = "dbname=nani_ai user=nani_user password=nani_pass host=localhost port=5432"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("❌ Database connection error:", str(e))
        return None  # Return None if connection fails


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class VideoQAPipeline:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VideoQAPipeline, cls).__new__(cls)
        return cls._instance

    def __init__(self, video_folder="videos", cache_dir="video_cache"):
        if hasattr(self, 'initialized'):
            return
        self.initialized = True

        self.video_folder = video_folder
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        #self.transcription_model = whisper.load_model("base", device=self.device)
        self.transcription_model = whisper.load_model("base", device="cpu")

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2",
                                    device=0 if torch.cuda.is_available() else -1)
        self.video_transcripts = self.preprocess_all_videos()

    def preprocess_all_videos(self):
        """Preprocess videos and store transcripts in the database."""
        conn = get_db_connection()
        cur = conn.cursor()

        video_transcripts = {}

        for video_filename in os.listdir(self.video_folder):
            if video_filename.endswith(('.mp4', '.avi', '.mov')):
                video_path = os.path.join(self.video_folder, video_filename)

                # Check if the video is already in the database
                cur.execute("SELECT transcript FROM videos WHERE filename = %s", (video_filename,))
                result = cur.fetchone()

                if result:
                    full_text = result[0]
                else:
                    transcription_data = self.process_video(video_path)
                    full_text = transcription_data.get("text", "")

                    # Insert into database
                    cur.execute(
                        "INSERT INTO videos (filename, transcript) VALUES (%s, %s) ON CONFLICT (filename) DO NOTHING",
                        (video_filename, full_text)
                    )
                    conn.commit()

                video_transcripts[video_filename] = full_text

        cur.close()
        conn.close()
        return video_transcripts

    def extract_audio(self, video_path):
        """Extracts audio from a video file using pydub."""
        audio_path = os.path.join(self.cache_dir, os.path.splitext(os.path.basename(video_path))[0] + ".wav")

        if not os.path.exists(audio_path):  # Extract only if not cached
            try:
                audio = AudioSegment.from_file(video_path, format="mp4")  # Auto-detect format
                audio = audio.set_channels(1).set_frame_rate(16000)
                audio.export(audio_path, format="wav")
                print(f"Extracted audio: {audio_path}")
            except Exception as e:
                print(f"Error extracting audio from {video_path}: {str(e)}")
                return None

        return audio_path

    def transcribe_audio(self, audio_path):
        return self.transcription_model.transcribe(audio_path)

    def process_video(self, video_path):
        """Extract audio from a video file and transcribe it."""
        audio_path = self.extract_audio(video_path)
        if audio_path:
            return self.transcribe_audio(audio_path)  # Use the extracted WAV file
        return {"text": ""}

    def get_embeddings(self, texts):
        return self.embedding_model.encode(texts)

    def select_videos(self, question, top_k=2):
        question_embedding = self.get_embeddings([question])
        video_transcripts_list = list(self.video_transcripts.values())
        video_names = list(self.video_transcripts.keys())

        video_embeddings = self.get_embeddings(video_transcripts_list)
        similarities = cosine_similarity(question_embedding, video_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [video_names[i] for i in top_indices]

    def answer_question(self, question):
        selected_video_names = self.select_videos(question)
        combined_context = " ".join([self.video_transcripts[video_name] for video_name in selected_video_names])
        answer = self.qa_pipeline(question=question, context=combined_context, max_answer_length=100)
        return {
            "answer": answer["answer"],
            "confidence": answer["score"],
            "context": combined_context,
            "selected_videos": selected_video_names
        }



qa_model = VideoQAPipeline()


@app.route("/api/ask", methods=["POST"])
def get_answer():
    data = request.json
    if "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    response = qa_model.answer_question(data["question"])
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    selected_influencers = data.get("selected_influencers", [])
    avatar = data.get("avatar", "")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, selected_influencers, avatar) VALUES (%s, %s, %s, %s)",
            (username, password_hash, selected_influencers, avatar)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({"error": "Username already exists"}), 409
    finally:
        cur.close()
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"error": "Invalid username or password"}), 401
