import cv2
import os
import tempfile
from typing import Union
from PIL import Image
from audio_extract import extract_audio
import whisper
from datetime import timedelta

class ExtractManager:
    def __init__(self):
        self.model = whisper.load_model("medium")

    def release(self):
        self.model = None

    def get_keyframe(self, video_path: Union[str, os.PathLike], start: float, end: float) -> Image.Image:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError("Không mở được video")

        fps = cap.get(cv2.CAP_PROP_FPS)
        mid_time = (start + end) / 2
        frame_num = int(mid_time * fps)

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        success, frame = cap.read()
        cap.release()

        if not success or frame is None:
            raise ValueError("Không lấy được frame")

        frame = cv2.resize(frame, (320, int(frame.shape[0] * 320 / frame.shape[1])))
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return image
    
    def get_transcript(self, video_path: Union[str, os.PathLike], start: float, end: float) -> str:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio:
            tmp_audio_path = tmp_audio.name

        try:
            start_time_str = seconds_to_time_str(start)

            if os.path.exists(tmp_audio_path):
                os.remove(tmp_audio_path)

            extract_audio(
                input_path=video_path,
                output_path=tmp_audio_path,
                start_time=start_time_str,
                duration=end - start
            )

            result = self.model.transcribe(tmp_audio_path, task="translate")
            return result["text"].strip()
        finally:
            if os.path.exists(tmp_audio_path):
                os.remove(tmp_audio_path)
                
def seconds_to_time_str(seconds: float) -> str:
        h = int(seconds) // 3600
        m = (int(seconds) % 3600) // 60
        s = int(seconds) % 60
        return f"{h:02}:{m:02}:{s:02}"