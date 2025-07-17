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
        self.processor = FlavaProcessor.from_pretrained("facebook/flava-full")
        self.model = FlavaModel.from_pretrained("facebook/flava-full").to(self.device)
        self.model.eval()

    def release(self):
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
            embedding = outputs.multimodal_projected_embedding[0]  

        emb = embedding.cpu().numpy()
        emb_norm = emb / np.linalg.norm(emb)

        return emb_norm
        

