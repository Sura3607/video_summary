import os
from pathlib import Path
import json
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.videoinfo import VideoInfo
from core.videoinfo import ImageInfo

def format_output_video(video_id: VideoInfo) -> None:
    data = VideoInfo.get_data(self=video_id)
    if not data or "video_id" not in data or "chunks" not in data:
        raise ValueError("Dữ liệu video không hợp lệ")
    
    video_id = data["video_id"]
    chunks = data["chunks"]

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{video_id}.json")

    formatted_chunks = []
    for c in chunks:
        if not c["vector"]:
            print(f"Cảnh báo: Chunk {c['meta']['chunk_index']} không có vector, sẽ bỏ qua.")
            continue
        
        if not c["summary"]:
            print(f"Cảnh báo: Chunk {c['meta']['chunk_index']} không có summary")
        
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
        
def format_output_image(image_info: ImageInfo) -> None:
    data = image_info.get_data()
    if not data or "image_id" not in data:
        raise ValueError("Dữ liệu ảnh không hợp lệ")

    if not data["vector"]:
        raise ValueError("Không thể lưu vì thiếu vector")

    if not data["summary"]:
        print("Cảnh báo: Ảnh không có summary")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{data['image_id']}.json")

    formatted_data = {
        "image_id": data["image_id"],
        "transcript": data["transcript"],
        "summary": data["summary"],
        "keywords": data["keywords"],
        "vector": data["vector"],
        "frame": data["frame"],
        "meta": data["meta"]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=2)