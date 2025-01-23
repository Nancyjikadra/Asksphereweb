import requests
import pickle
import io
import logging

def download_model_from_drive(drive_shareable_link):
    """
    Download model from Google Drive shareable link
    
    Args:
        drive_shareable_link (str): Shareable Google Drive link
    
    Returns:
        Loaded pickle model
    """
    try:
        # Extract file ID from shareable link
        file_id = drive_shareable_link.split('/d/')[1].split('/')[0]
        download_url = f'https://drive.google.com/uc?id={file_id}'
        
        # Download model
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Load model from bytes
        model = pickle.load(io.BytesIO(response.content))
        logging.info("Model successfully downloaded and loaded")
        return model
    
    except Exception as e:
        logging.error(f"Model download failed: {e}")
        raise
