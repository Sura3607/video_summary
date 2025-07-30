from transformers import pipeline,BlipProcessor, BlipForConditionalGeneration
from keybert import KeyBERT
from typing import List
from PIL import Image
import torch
     
class EnrichManager:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model_captioning = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)
        self.model_keyword = KeyBERT()
    def release(self):
        self.model_captioning = None
        self.model_keyword = None

    