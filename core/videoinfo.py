import base64
import io
from PIL import Image

class VideoInfo:
    def __init__(self, video_id: str, source_path: str, duration: float):
        self.data = {
            "video_id": video_id,
            "source_path": source_path,
            "duration": duration,
            "chunks": []
        }

    def add_chunks(self, chunks: list[dict]):
        for i, c in enumerate(chunks):
            self.data["chunks"].append({
                "start": c["start"],
                "end": c["end"],
                "transcript": None,
                "summary": None,
                "keywords": [],
                "vector": [],
                "frame": None,
                "meta": {
                    "chunk_index": i,
                    "length": round(c["end"] - c["start"], 2)
                }
            })

    def add_transcripts(self, transcripts: list[str]):
        for chunk, t in zip(self.data["chunks"], transcripts):
            chunk["transcript"] = t

    def add_summaries(self, summaries: list[str]):
        for chunk, s in zip(self.data["chunks"], summaries):
            chunk["summary"] = s

    def add_keywords(self, keywords_list: list[list[str]]):
        for chunk, kw in zip(self.data["chunks"], keywords_list):
            chunk["keywords"] = kw

    def add_vectors(self, vectors: list[list[float]]):
        for chunk, v in zip(self.data["chunks"], vectors):
            chunk["vector"] = v

    def add_frames(self, frames: list[Image.Image]):
        for chunk, img in zip(self.data["chunks"], frames):
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
            chunk["frame"] = f"data:image/jpeg;base64,{encoded}"

    def get_data(self):
        return self.data
    
class ImageInfo:
    def __init__(self, image_id: str, source_path: str):
        self.data = {
            "image_id": image_id,
            "source_path": source_path,
            "transcript": None,
            "summary": None,
            "keywords": [],
            "vector": [],
            "frame": None,
            "meta": {}
        }

    def add_transcript(self, t: str):
        self.data["transcript"] = t

    def add_summary(self, s: str):
        self.data["summary"] = s

    def add_keywords(self, kw: list[str]):
        self.data["keywords"] = kw

    def add_vector(self, vec: list[float]):
        self.data["vector"] = vec

    def add_frame(self, img: Image.Image):
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.data["frame"] = f"data:image/jpeg;base64,{encoded}"

    def get_data(self):
        return self.data
