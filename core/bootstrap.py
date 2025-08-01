from core.embed import EmbeddingManager
from core.enrich import KeywordExtractor, CaptionImage
from core.extract import ExtractManager
from config.config import load_config

class ModelRegistry:
    embedding_manager: EmbeddingManager = None
    keyword_extractor: KeywordExtractor = None
    caption_image: CaptionImage = None
    extract_manager: ExtractManager = None

def load_embedding_model(model_name: str):
    ModelRegistry.embedding_manager = EmbeddingManager().load(model_name=model_name)

def load_keyword_model():
    ModelRegistry.keyword_extractor = KeywordExtractor().load()

def load_caption_model(model_name: str):
    ModelRegistry.caption_image = CaptionImage().load(model_name=model_name)

def load_extract_model(model_name: str):
    ModelRegistry.extract_manager = ExtractManager().load(model_name=model_name)

def load_all_models():
    config = load_config(config_path="config/config.yml")
    load_embedding_model(config["Embedding"]["name"])
    load_keyword_model()
    load_caption_model(config["Caption"]["name"])
    load_extract_model(config["Extract"]["name"])

    
    