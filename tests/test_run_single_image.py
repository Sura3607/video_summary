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


def test_process_single_image(img_path, output_dir):

    try:
        # Process the image
        process_single_image(img_path, output_dir)
        print(f"Successfully processed image: {img_path}")
    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    config = load_config("config/config.yaml")
    bootstrap.load_embedding_model(config["Embedding"]["name"])
    bootstrap.load_caption_model(config["Captioner"]["name"])

    img_path = r"data\1_06b289b7531c20620e1dd8f10dc73beb.png"
    output_dir = "output"

    test_process_single_image(img_path, output_dir)



