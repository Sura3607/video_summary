from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core.videoinfo import VideoInfo,ImageInfo
from core.formatter import format_output_video, format_output_image
import json
from pathlib import Path
from PIL import Image

def test_format_output_video():
    vid = VideoInfo("demo_video", "path", 30.0)
    vid.add_chunks([{"start": 0, "end": 10}, {"start": 10, "end": 20}])
    vid.add_transcripts(["Hello world", "How are you?"])
    vid.add_summaries(["Greeting", ""])
    vid.add_keywords([["hello", "world"], ["how", "you"]])
    vid.add_vectors([[0.1, 0.2], []])

    dummy_img = Image.new("RGB", (100, 100), color="red")
    vid.add_frames([dummy_img, dummy_img])

    format_output_video(vid, "output")

    path = Path("output/demo_video.json")
    assert path.exists(), "Output file không tồn tại"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # print json data
        print(json.dumps(data, ensure_ascii=False, indent=2))

    assert isinstance(data, list) and len(data) == 1, "Dữ liệu JSON sai"
    for item in data:
        for field in ["timestamp", "transcript", "summary", "keywords", "vector", "frame", "meta"]:
            assert field in item, f"Thiếu field: {field}"
        assert item["frame"].startswith("data:image/jpeg;base64,")

    print("Test passed for format_output with VideoInfo")
    
def test_format_output_image():
    img = ImageInfo("demo_image", "path/to/image.jpg")
    dummy_img = Image.new("RGB", (100, 100), color="blue")

    img.add_image(dummy_img)  
    img.add_caption("Sample image caption")  
    img.add_vector([0.1, 0.2, 0.3])

    format_output_image(img, "output")

    path = Path("output/demo_image.json")
    assert path.exists(), "Output file không tồn tại"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        print(json.dumps(data, ensure_ascii=False, indent=2))

    for field in ["id", "path", "caption", "size", "vector", "image"]:
        assert field in data, f"Thiếu field: {field}"
    assert data["image"].startswith("data:image/jpeg;base64,")

    print("Test passed for format_output_image")


if __name__ == "__main__":
    test_format_output_video()
    test_format_output_image()
    sys.exit(0)
#  pytest tests/test_formatter.py -v
#  Output: test_format_output PASSED