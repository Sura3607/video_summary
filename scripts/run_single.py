import os
import json
from PIL import Image
from pathlib import Path
from core import bootstrap
from core.helper import load_config
from core.bootstrap import load_all_models, ModelRegistry
from core.chunking import split_video_into_chunks
from core.info import VideoInfo, ImageInfo
from core.formatter import format_output_video, format_output_image

def process_single_video(input_path: str, output_path: str):
    # 2. Split video into chunks
    chunks = split_video_into_chunks(input_path)
    
    # 3. Initialize VideoInfo
    video_id = Path(input_path).stem
    duration = chunks[-1]["end"] if chunks else 0
    video_info = VideoInfo(video_id, input_path, duration)
    video_info.add_chunks(chunks)
    
    # 4. Extract audio transcripts and keyframes
    frames =[]
    transcripts = []
    for chunk in chunks:
        start = chunk["start"]
        end = chunk["end"]
        
        # Get keyframe,transcript for the chunk
        frame = None
        transcript = ""
        try:
            frame = ModelRegistry.extract_manager.get_keyframe(input_path, start, end)
            transcript = ModelRegistry.extract_manager.get_transcript(input_path, start, end)
        except Exception as e:
            raise RuntimeError(f"Error extracting data for chunk {start}-{end}: {e}")
        finally:
            frames.append(frame)
            transcripts.append(transcript)
        
    # 5. Generate embeddings
    vectors = []
    for frame, transcript in zip(frames, transcripts):
        if frame is None or transcript is None:
            raise ValueError("Frame or transcript is None, cannot generate embedding.")
        try:
            if not isinstance(frame, Image.Image):
                raise TypeError("Frame is not a PIL Image.")
            if not isinstance(transcript, str) or len(transcript) == 0:
                raise ValueError("Transcript is empty.")
            vector = ModelRegistry.embedding_manager.start(transcript, frame)
            vectors.append(vector)
        except Exception as e:
            raise RuntimeError(f"Error generating embedding for chunk: {e}")
    
    # 6. Enrich with summaries and keywords
    captions = []
    keywords = []

    for frame, transcript in zip(frames, transcripts):
        if frame is None or transcript is None:
            raise ValueError("Frame or transcript is None, cannot enrich.")
        try:
            caption = ModelRegistry.caption_image.captioning(frame)
            keyword_list = ModelRegistry.keyword_extractor.extract_keywords(transcript)
            captions.append(caption)
            keywords.append(keyword_list)
        except Exception as e:
            raise RuntimeError(f"Error enriching data for chunk: {e}")
    
    # 7. Add all data to VideoInfo
    video_info.add_transcripts(transcripts)
    video_info.add_summaries(captions)
    video_info.add_keywords(keywords)
    video_info.add_vectors(vectors)
    video_info.add_frames(frames)

    # 8. Save results to JSON
    format_output_video(video_info, output_path)

def process_single_image(input_path: str, output_path: str):
    # 1. Initialize ImageInfo
    image_id = Path(input_path).stem
    image_info = ImageInfo(image_id, input_path)

    # 2. Load and process the image
    try:
        image = Image.open(input_path).convert("RGB")
    except Exception as e:
        raise RuntimeError(f"Error loading image {input_path}: {e}")

    # 3. Generate caption
    try:
        caption = ModelRegistry.caption_image.captioning(image)
        image_info.add_caption(caption)
    except Exception as e:
        raise RuntimeError(f"Error generating caption: {e}")

    # 4. Generate embedding vector
    try:
        vector = ModelRegistry.embedding_manager.start(caption, image)
        image_info.add_vector(vector)
    except Exception as e:
        raise RuntimeError(f"Error generating embedding: {e}")

    # 5. Add the original image
    image_info.add_image(image)

    # 6. Save results to JSON
    try:
        format_output_image(image_info, output_path)
    except Exception as e:
        raise RuntimeError(f"Error saving output: {e}")

