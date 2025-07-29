import torch
import numpy as np
from transformers import FlavaProcessor, FlavaModel
from PIL import Image
from typing import Union
from torchvision import transforms

class EmbeddingManager:
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load()

    def load(self):
        if self.model is not None:
            return
        
        try:
            self.processor = FlavaProcessor.from_pretrained("facebook/flava-full")
            self.model = FlavaModel.from_pretrained("facebook/flava-full").to(self.device)
            self.model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to load FLAVA model: {e}")

    def release(self):
        if self.model is None or self.processor is None:
            raise RuntimeError("Model is not loaded. Cannot release resources.")
        self.model = None
        self.processor = None
        torch.cuda.empty_cache()

    def start(self, text: str, image: Union[str, Image.Image]) -> np.ndarray:
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif isinstance(image, Image.Image):
            image = image.convert("RGB")
        else:
            raise ValueError("Image must be a file path or a PIL Image object.")
        
        inputs = self.processor(text=text, images=image, return_tensors="pt", padding=True).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            sequence_emb = outputs.multimodal_embeddings[0]

        pooled = sequence_emb.mean(dim=0)  # shape (768,)
        pooled_np = pooled.cpu().numpy()
        normalized = pooled_np / np.linalg.norm(pooled_np)

        return normalized
        

