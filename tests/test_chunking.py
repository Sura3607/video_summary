from core.chunking import split_video_into_chunks

def test_split_video():
    test_video_path = r'D:\Project_Management\video_summary\data\Luckiest People Alive!.mp4'
    scenes = split_video_into_chunks(test_video_path,30)    

    assert isinstance(scenes, list)
    assert all(isinstance(s, dict) and 'start' in s and 'end' in s for s in scenes)

    for i, scene in enumerate(scenes):
        duration = scene['end'] - scene['start']
        assert duration >= 2.0, f"Scene {i} quá ngắn ({duration}s)"
        if i > 0:
            assert scene['start'] >= scenes[i-1]['end'], f"Scene {i} bị trùng timestamp với scene trước"

        print(f"Scene {i}: start = {scene['start']:.3f}s, end = {scene['end']:.3f}s, duration = {duration:.3f}s")

if __name__ == "__main__":
    test_split_video()

# Output:
# VideoManager is deprecated and will be removed.
# Scene 0: start = 0.000s, end = 2.600s, duration = 2.600s
# Scene 1: start = 3.967s, end = 6.433s, duration = 2.466s
# Scene 2: start = 6.433s, end = 8.767s, duration = 2.334s
# Scene 3: start = 16.633s, end = 18.733s, duration = 2.100s
# Scene 4: start = 24.567s, end = 26.900s, duration = 2.333s
# Scene 5: start = 26.900s, end = 31.800s, duration = 4.900s
# Scene 6: start = 31.800s, end = 37.667s, duration = 5.867s
# Scene 7: start = 44.833s, end = 48.767s, duration = 3.934s
# Scene 8: start = 48.767s, end = 55.400s, duration = 6.633s
# Scene 9: start = 55.400s, end = 60.367s, duration = 4.967s
# Scene 10: start = 61.433s, end = 63.567s, duration = 2.134s
# ...
# Scene 60: start = 358.033s, end = 363.300s, duration = 5.267s
# Scene 61: start = 363.300s, end = 367.633s, duration = 4.333s
# Scene 62: start = 367.633s, end = 370.067s, duration = 2.434s
# Scene 63: start = 370.067s, end = 372.167s, duration = 2.100s
# Scene 64: start = 375.500s, end = 377.733s, duration = 2.233s
# Scene 65: start = 377.733s, end = 380.067s, duration = 2.334s
# Scene 66: start = 382.667s, end = 387.633s, duration = 4.966s
# Scene 67: start = 388.900s, end = 391.633s, duration = 2.733s
# Scene 68: start = 392.400s, end = 394.500s, duration = 2.100s
# Scene 69: start = 397.433s, end = 402.133s, duration = 4.700s
# Scene 70: start = 402.133s, end = 404.567s, duration = 2.434s
# Scene 71: start = 408.767s, end = 413.200s, duration = 4.433s
# Scene 72: start = 413.200s, end = 415.833s, duration = 2.633s