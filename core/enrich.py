from transformers import pipeline,BlipProcessor, BlipForConditionalGeneration,AutoTokenizer
from keybert import KeyBERT
from typing import List
from PIL import Image
import torch

     
class CaptionImage:
    def __init__(self, model, processor, tokenizer, device):
        self.device = device
        self.model_captioning = model
        self.processor = processor
        self.tokenizer = tokenizer

    @classmethod
    def load(cls, model_name="Salesforce/blip-image-captioning-base", device=None):
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        try:
            processor = BlipProcessor.from_pretrained(model_name)
            model_captioning = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
            model_captioning.eval()
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            return cls(model_captioning, processor, tokenizer, device)
        except Exception as e:
            raise RuntimeError(f"Model Captioning loading failed: {e}")
        
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
    def __init__(self,model,device):
        self.device = device
        self.model = model
        
    @classmethod
    def load(cls):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            model = KeyBERT()
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")
        return cls(model, device)

    def release(self):
        self.model = None
        self.device = None
        torch.cuda.empty_cache()

    def extract_keywords(self, text: str) -> List[str]:
        keywords = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=5
        )
        return [kw for kw, _ in keywords]