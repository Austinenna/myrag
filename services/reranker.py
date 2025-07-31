from typing import List, Tuple
from sentence_transformers import CrossEncoder


class Reranker:
    """重排序器，负责对检索结果进行重新排序"""
    
    def __init__(self, model_name: str = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'):
        """初始化重排序器
        
        Args:
            model_name: CrossEncoder模型名称
        """
        self.model_name = model_name
        self.cross_encoder = CrossEncoder(model_name)
    
    def rerank(self, query: str, documents: List[str], top_k: int) -> List[str]:
        """对文档进行重排序
        
        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回的文档数量
            
        Returns:
            重排序后的文档列表
        """
        if not documents:
            return []
        
        # 创建查询-文档对
        pairs = [(query, doc) for doc in documents]
        
        # 计算相关性分数
        scores = self.cross_encoder.predict(pairs)
        
        # 将文档和分数配对并排序
        scored_documents = list(zip(documents, scores))
        scored_documents.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前top_k个文档
        return [doc for doc, _ in scored_documents[:top_k]]
    
    def rerank_with_scores(self, query: str, documents: List[str], top_k: int) -> List[Tuple[str, float]]:
        """对文档进行重排序并返回分数
        
        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回的文档数量
            
        Returns:
            重排序后的文档和分数列表
        """
        if not documents:
            return []
        
        # 创建查询-文档对
        pairs = [(query, doc) for doc in documents]
        
        # 计算相关性分数
        scores = self.cross_encoder.predict(pairs)
        
        # 将文档和分数配对并排序
        scored_documents = list(zip(documents, scores))
        scored_documents.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前top_k个文档和分数
        return scored_documents[:top_k]
    
    def get_model_info(self) -> dict:
        """获取模型信息
        
        Returns:
            模型信息字典
        """
        return {
            "model_name": self.model_name,
            "max_length": getattr(self.cross_encoder, 'max_length', 'Unknown')
        }