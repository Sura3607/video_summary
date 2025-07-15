from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def split_video_into_chunks(vide_path: str, threshold:int = 30) -> list[dict[str,float]]:
    """
    Chưa viết mô tả
    """
    video_manager = VideoManager([vide_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    try:
        video_manager.set_downscale_factor()
        video_manager.start()

        scene_manager.detect_scenes(frame_source=video_manager)

        scene_list = scene_manager.get_scene_list()

        chunks = []
        for i, (start_time, end_time) in enumerate(scene_list):
            start_sec = start_time.get_seconds()
            end_sec = end_time.get_seconds()

            # Bỏ cảnh < 2s
            if end_sec - start_sec >= 2.0:
                chunks.append({
                    'start': round(start_sec, 3),
                    'end': round(end_sec, 3)
                })

        for i in range(1, len(chunks)):
            assert chunks[i]['start'] >= chunks[i-1]['end'], "Cảnh bị trùng!"
            assert chunks[i]['start'] > chunks[i-1]['start'], "Cảnh không tuần tự!"

        return chunks

    finally:
        video_manager.release()