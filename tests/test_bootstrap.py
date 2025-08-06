import os
import sys
import pytest
from PIL import Image
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import bootstrap
from core.bootstrap import ModelRegistry


@pytest.fixture(scope="session", autouse=True)
def setup_models():
    bootstrap.load_all_models("config/config.yaml")
    return ModelRegistry


def test_embedding_manager(setup_models):
    embedding_manager = setup_models.embedding_manager
    assert embedding_manager is not None

    text = "A cat sitting on a chair."
    image = Image.new("RGB", (32, 32), color="white")
    emb = embedding_manager.start(text, image)

    assert isinstance(emb, np.ndarray)
    assert emb.shape[0] == 768


def test_caption_image(setup_models):
    captioner = setup_models.caption_image
    assert captioner is not None

    image = Image.new("RGB", (32, 32), color="white")
    caption = captioner.captioning(image)

    assert isinstance(caption, str)
    assert len(caption) > 0


def test_keyword_extraction(setup_models):
    extractor = setup_models.keyword_extractor
    assert extractor is not None

    text = "The quick brown fox jumps over the lazy dog."
    keywords = extractor.extract_keywords(text)

    assert isinstance(keywords, list)
    assert len(keywords) > 0


def test_extract_manager(setup_models):
    extract_manager = setup_models.extract_manager
    assert extract_manager is not None

    pass


if __name__ == "__main__":
    pytest.main([__file__])

