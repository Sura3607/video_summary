import os
import sys
import numpy as np
from PIL import Image
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.embed import EmbeddingManager
from core.chunking import split_video_into_chunks
from core.extract import ExtractManager

SAMPLE_VIDEO = r""

@pytest.mark.skipif(not os.path.exists(SAMPLE_VIDEO), reason="Sample video not found.")
def test_embedding_on_video_chunk():
    # Split video into chunks
    chunks = split_video_into_chunks(SAMPLE_VIDEO, threshold=30)
    assert len(chunks) > 0, "No chunks detected in video."

    # Use the first chunk for testing
    chunk = chunks[0]
    start, end = chunk['start'], chunk['end']

    # Extract keyframe and transcript
    extract_mgr = ExtractManager()
    keyframe = extract_mgr.get_keyframe(SAMPLE_VIDEO, start, end)
    transcript = extract_mgr.get_transcript(SAMPLE_VIDEO, start, end)
    assert isinstance(keyframe, Image.Image), "Keyframe is not a PIL Image."
    assert isinstance(transcript, str) and len(transcript) > 0, "Transcript is empty."

    # Generate embedding
    embed_mgr = EmbeddingManager()
    emb = embed_mgr.start(transcript, keyframe)
    assert isinstance(emb, np.ndarray), "Embedding is not a numpy array."
    assert emb.shape[0] > 0, "Embedding is empty."
    assert np.isclose(np.linalg.norm(emb), 1.0, atol=1e-3), "Embedding is not normalized."

    # Release resources
    embed_mgr.release()
    extract_mgr.release()
