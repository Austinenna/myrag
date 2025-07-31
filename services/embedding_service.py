from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """嵌入服务，负责文本的向量化处理"""
    
    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        """初始化嵌入服务
        
        Args:
            model_name: 嵌入模型名称
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> List[float]:
        """将单个文本转换为嵌入向量
        
        Args:
            text: 输入文本
            
        Returns:
            嵌入向量
        """
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量将文本转换为嵌入向量
        
        Args:
            texts: 文本列表
            
        Returns:
            嵌入向量列表
        """
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return [embedding.tolist() for embedding in embeddings]
    
    def get_model_info(self) -> dict:
        """获取模型信息
        
        Returns:
            模型信息字典
        """
        return {
            "model_name": self.model_name,
            "max_seq_length": self.model.max_seq_length,
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        }