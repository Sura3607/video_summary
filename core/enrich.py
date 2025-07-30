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

    def captioning(self, image: Image.Image) -> str:
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        out = self.model_captioning.generate(**inputs, max_length=30)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption.strip()
    
    def extract_keywords(self, text: str) -> List[str]:
        keywords = self.model_keyword.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=5
        )
        return [kw for kw, _ in keywords]