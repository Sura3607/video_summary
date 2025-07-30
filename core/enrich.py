from transformers import pipeline,BlipProcessor, BlipForConditionalGeneration,AutoTokenizer
from keybert import KeyBERT
from typing import List
from PIL import Image
import torch

     
class CaptionImage:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_captioning = None
        self.processor = None
        self.load()
        pass
    
    def load(self):
        if self.model_captioning is not None and self.processor is not None and self.model_keyword is not None:
            return  

        try:
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.model_captioning = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(self.device)
            self.model_captioning.eval()
            self.model_keyword = KeyBERT()
            self.tokenizer = AutoTokenizer.from_pretrained("Salesforce/blip-image-captioning-base")
        except Exception as e:
            print(f"[Error] Failed to load models in EnrichManager: {e}")
            raise RuntimeError(f"Model loading failed: {e}")
        
    def release(self):
        self.model_captioning = None
        self.processor = None
        torch.cuda.empty_cache()

    def captioning(self, image: Image.Image) -> str:
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        out = self.model_captioning.generate(**inputs, max_length=30)
        tokenizer = self.tokenizer
        caption = tokenizer.decode(out[0], skip_special_tokens=True)
        return caption.strip()
    
    
class KeywordExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.load()
        
    def load(self):
        if self.model is not None:
            return  
        try:
            self.model = KeyBERT()
        except Exception as e:
            print(f"[Error] Failed to load models in KeywordExtractor: {e}")
            raise RuntimeError(f"Model loading failed: {e}")
        
    def release(self):
        self.model = None
        torch.cuda.empty_cache()

    def extract_keywords(self, text: str) -> List[str]:
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=5
        )
        return [kw for kw, _ in keywords]