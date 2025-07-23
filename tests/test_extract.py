from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.extract import ExtractManager

extractor = ExtractManager()
video_path = Path(r"C:/Users/Acer/source/repos/AIC_2025/Everyday English Conversation Practice ｜ 30 Minutes English Listening.mp4")
start, end = 5, 10

def test_keyframe():
    frame = extractor.get_keyframe(video_path, start, end)
    assert frame is not None, "Frame is None"
    frame.show()
    print("Keyframe extracted successfully.")

def test_transcript():
    transcript = extractor.get_transcript(video_path, start, end)
    assert transcript.strip() != "", "Transcript is empty"
    print("Transcript:")
    print(transcript)

if __name__ == "__main__":
    test_keyframe()
    test_transcript()
