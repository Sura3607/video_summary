from core.embed import EmbeddingManager
from core.enrich import KeywordExtractor, CaptionImage
from core.extract import ExtractManager
from config.config import load_config

class ModelRegistry:
    embedding_manager: EmbeddingManager = None
    keyword_extractor: KeywordExtractor = None
    caption_image: CaptionImage = None
    extract_manager: ExtractManager = None

def load_all_models():
    config = load_config(config_path="config/config.yml")
    ModelRegistry.embedding_manager = EmbeddingManager().load(model_name=config["Embedding"]["name"])
    ModelRegistry.keyword_extractor = KeywordExtractor().load()
    ModelRegistry.caption_image = CaptionImage().load()
    # ModelRegistry.extract_manager = ExtractManager().load()

    
    