from pathlib import Path
import os
import pytest 
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.enrich import CaptionImage,KeywordExtractor
from core.extract import ExtractManager
video_path = Path(r"C:/Users/Acer/source/repos/AIC_2025/Everyday English Conversation Practice ｜ 30 Minutes English Listening.mp4")
start, end = 5, 10

extractor = ExtractManager()
keyframe = extractor.get_keyframe(video_path, start, end)

def test_caption():
    if keyframe is None:
        print("Không trích xuất được keyframe.")
        return
    enricher_cap = CaptionImage()
    caption = enricher_cap.captioning(keyframe)
    print("Caption:", caption)
    enricher_cap.release()
 
def test_keyword_extractor():
    enricher_keyw = KeywordExtractor()
    transcript = extractor.get_transcript(video_path, start, end)
    if not transcript.strip():
        print("Không có transcript.")
        return
    print("Transcript:", transcript)
    keywords = enricher_keyw.extract_keywords(transcript)
    print("Keywords:", keywords)
    enricher_keyw.release()
    
if __name__ == "__main__":
    test_caption()
    test_keyword_extractor()
    sys.exit(0)
    
# Output:
# Caption: [Caption: a cartoon character with a speech bubble that says hello welcome to english practice]
# Transcript: Hello, welcome to the English Easy.
# Keywords: ['welcome english', 'english easy', 'hello', 'hello welcome', 'english']
# pytest tests/test_enrich.py -s 
# Output: passed