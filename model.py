import os
import numpy as np
import torch
import json
from transformers import pipeline, AutoTokenizer
import whisper
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import librosa
from moviepy.editor import VideoFileClip
import logging


class VideoQAPipeline:
    def __init__(self, cache_dir="video_cache"):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        # Load tokenizer and model explicitly
        self.tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        # Initialize models
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"Using device: {self.device}")
        self.transcription_model = whisper.load_model("base", device=self.device)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", device=0 if torch.cuda.is_available() else -1)

        self.logger.info("Models loaded successfully")

    def extract_audio(self, video_path):
        """Extract audio from a video file."""
        try:
            audio_array, _ = librosa.load(video_path, sr=16000, mono=True)
            return audio_array.astype(np.float32)
        except Exception as e:
            self.logger.error(f"Librosa failed: {e}. Trying moviepy...")
            try:
                video = VideoFileClip(video_path)
                audio = video.audio
                audio_array = audio.to_soundarray(fps=16000)
                if len(audio_array.shape) > 1:
                    audio_array = audio_array.mean(axis=1)  # Convert stereo to mono
                video.close()
                return audio_array.astype(np.float32)
            except Exception as e:
                self.logger.error(f"Moviepy failed: {e}")
                raise ValueError("Failed to extract audio from the video.")

    # Add other methods as needed
