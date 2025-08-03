import os
import json
from core.videoinfo import VideoInfo

def format_ouptput(video_id: VideoInfo, chunk_data: VideoInfo) -> None:
    data = VideoInfo.get_data()
    video_id = data["video_id"]
    chunks = data["chunks"]

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{video_id}.json")

    formatted_chunks = []
    for c in chunks:
        formatted_chunks.append({
            "timestamp": f"{c['start']:.2f} - {c['end']:.2f}",
            "transcript": c["transcript"],
            "summary": c["summary"],
            "keywords": c["keywords"],
            "vector": c["vector"],
            "frame": c["frame"],
            "meta": c["meta"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(formatted_chunks, f, ensure_ascii=False, indent=2)