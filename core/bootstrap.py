from core.embed import EmbeddingManager
from core.enrich import KeywordExtractor, CaptionImage
from core.extract import ExtractManager

class ModelRegistry:
    embedding_manager: EmbeddingManager = None
    keyword_extractor: KeywordExtractor = None
    caption_image: CaptionImage = None
    extract_manager: ExtractManager = None



def load_all_models():
    ModelRegistry.embedding_manager = EmbeddingManager().load()
    ModelRegistry.keyword_extractor = KeywordExtractor().load()
    ModelRegistry.caption_image = CaptionImage().load()
    ModelRegistry.extract_manager = ExtractManager().load()

    
    