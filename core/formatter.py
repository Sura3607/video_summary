import os
from pathlib import Path
import json
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.info import VideoInfo
from core.info import ImageInfo

def format_output_video(video_id: VideoInfo,output_path: str) -> None:
    data = VideoInfo.get_data(self=video_id)
    if not data or "video_id" not in data or "chunks" not in data:
        raise ValueError("Dữ liệu video không hợp lệ")
    
    video_id = data["video_id"]
    chunks = data["chunks"]

    os.makedirs(output_path, exist_ok=True)
    output_path = os.path.join(output_path, f"{video_id}.json")

    formatted_chunks = []
    for c in chunks:
        if c["vector"] is None or len(c["vector"]) == 0:
            raise ValueError("Vector không hợp lệ")

        if c["summary"] is None or len(c["summary"]) == 0:
            raise ValueError("Summary không hợp lệ")
        
        formatted_chunks.append({
            "timestamp": f"{c['start']:.2f} - {c['end']:.2f}",
            "transcript": c["transcript"],
            "summary": c["summary"],
            "keywords": c["keywords"],
            "vector": c["vector"],
            "frame": c["frame"],
            "meta": c["meta"]
        })
    if not formatted_chunks:
        raise ValueError("Không thể xuất dữ liệu do có chunk không có vector")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_chunks, f, ensure_ascii=False, indent=2)
        
def format_output_image(image_info: ImageInfo, output_path: str) -> None:
    data = image_info.get_data()
    if not data or "id" not in data:
        raise ValueError("Dữ liệu ảnh không hợp lệ")

    if data["vector"] is None or len(data["vector"]) == 0:
        raise ValueError("Không thể lưu vì thiếu vector")

    if data["caption"] is None or len(data["caption"]) == "":
        print("Cảnh báo: Ảnh không có caption")

    os.makedirs(output_path, exist_ok=True)
    output_path = os.path.join(output_path, f"{data['id']}.json")

    formatted_data = {
        "id": data["id"],
        "path": data["path"],
        "caption": data.get("caption", ""),
        "size": data.get("size", None),
        "vector": data["vector"],
        "image": data.get("image", None),
        "meta": data.get("meta", {})
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)
