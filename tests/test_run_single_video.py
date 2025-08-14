import os
import sys
import json
import pytest
from pathlib import Path
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.run_single import process_single_video, process_single_image
from core import bootstrap
from core.helper import load_config


def test_process_single_video(video_path, output_dir):
    try:
        # Process the video
        process_single_video(video_path, output_dir)
        
        # Check if output file was created
        output_file = Path(output_dir) / f"{Path(video_path).stem}.json"
        assert output_file.exists(), "Output JSON file was not created"
            
        print(f"Successfully processed video: {video_path}")
        print(f"Created output file: {output_file}")
        
    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")


if __name__ == "__main__":
    config = load_config("config/config.yaml")
    bootstrap.load_embedding_model(config["Embedding"]["name"])
    bootstrap.load_keyword_model()
    bootstrap.load_caption_model(config["Captioner"]["name"])
    bootstrap.load_extract_model(config["Transcriber"]["name"])

    video_path = r"data/Everyday English Conversation Practice ｜ 10 Minutes English Listening.mp4"
    output_dir = "output"

    test_process_single_video(video_path, output_dir)



