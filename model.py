import os
import numpy as np
import torch
import json
from transformers import pipeline
import whisper
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import librosa
from moviepy.editor import VideoFileClip
import pickle
import logging

class VideoQAPipeline:
    def __init__(self, cache_dir="video_cache"):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            # Use a more robust transcription model
            self.transcription_model = whisper.load_model("base", device=self.device)
            
            # Use a different embedding model if one fails
            self.embedding_model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
            
            self.qa_pipeline = pipeline(
                "question-answering", 
                model="deepset/roberta-base-squad2", 
                device=-1
            )
        except Exception as e:
            self.logger.error(f"Model initialization error: {e}")
            raise

    def extract_audio(self, video_path):
        """Robust audio extraction method."""
        try:
            # Try librosa first
            audio_array, _ = librosa.load(video_path, sr=16000, mono=True)
            return audio_array.astype(np.float32)
        except Exception as librosa_error:
            self.logger.warning(f"Librosa failed: {librosa_error}. Trying moviepy...")
            try:
                # Fallback to moviepy
                video = VideoFileClip(video_path)
                audio = video.audio
                audio_array = audio.to_soundarray(fps=16000)
                
                # Convert stereo to mono if needed
                if len(audio_array.shape) > 1:
                    audio_array = audio_array.mean(axis=1)
                
                video.close()
                return audio_array.astype(np.float32)
            except Exception as moviepy_error:
                self.logger.error(f"Audio extraction completely failed: {moviepy_error}")
                return np.zeros(16000, dtype=np.float32)  # Return silence instead of raising error

    def transcribe_audio(self, audio_array):
        """Transcribe audio with fallback."""
        try:
            return self.transcription_model.transcribe(audio_array)
        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return {"text": ""}

    def process_video(self, video_path):
        """Process video with comprehensive error handling."""
        try:
            audio_array = self.extract_audio(video_path)
            return self.transcribe_audio(audio_array)
        except Exception as e:
            self.logger.error(f"Video processing failed for {video_path}: {e}")
            return {"text": ""}

    def get_embeddings(self, texts):
        """Robust embedding generation."""
        if not texts:
            return np.zeros((0, 384))  # Match embedding dimension
        
        try:
            # Clean texts
            cleaned_texts = [str(text).strip() for text in texts if text]
            if not cleaned_texts:
                return np.zeros((0, 384))
            
            return self.embedding_model.encode(cleaned_texts)
        except Exception as e:
            self.logger.error(f"Embedding generation failed: {e}")
            return np.zeros((len(texts), 384))

    def answer_questions(self, questions, video_paths):
        """Robust question answering."""
        responses = {}
        
        # Process all videos
        all_texts = []
        for video_path in video_paths:
            if not os.path.exists(video_path):
                self.logger.warning(f"Video path not found: {video_path}")
                continue
            
            transcription = self.process_video(video_path)
            text = transcription.get("text", "")
            if text:
                all_texts.append(text)
        
        # Fallback context if no videos processed
        combined_context = " ".join(all_texts) if all_texts else "No video context available."

        for question in questions:
            try:
                # Attempt to answer with context
                answer = self.qa_pipeline(
                    question=question, 
                    context=combined_context,
                    max_answer_length=100
                )
                
                responses[question] = {
                    "answer": answer.get("answer", "Could not generate an answer."),
                    "confidence": answer.get("score", 0.0)
                }
            except Exception as e:
                self.logger.error(f"Question answering failed: {e}")
                responses[question] = {
                    "answer": "An error occurred while processing the question.",
                    "confidence": 0.0
                }
        
        return responses


# Example usage
if __name__ == "__main__":
    video_paths = ["/content/videoplayback.mp4","/content/videoplayback (2).mp4"]
    questions = [
        "where is she living?",
        "what is she having in lunch?",
        "why is she cooking?",
        "how swarty house looks like?",
        "what is she cooking?"
    ]

    pipeline = VideoQAPipeline()

        # Save the model to a pickle file
    with open('model.pkl', 'wb') as f:
        pickle.dump(pipeline, f)

    print("Model saved as 'model.pkl'")
    results = pipeline.answer_questions(questions, video_paths)

   # results = pipeline.answer_questions(questions, video_paths)

    for question, result in results.items():
        print(f"Question: {question}")
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")
        print("-" * 50)
