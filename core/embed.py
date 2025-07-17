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
        
        

