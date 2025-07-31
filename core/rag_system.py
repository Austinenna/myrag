from typing import List, Optional
from .document_processor import DocumentProcessor
from .vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.reranker import Reranker
from services.generator import Generator


class RAGSystem:
    """RAG系统主类，整合所有功能模块"""
    
    def __init__(self, 
                 embedding_model: str = "shibing624/text2vec-base-chinese",
                 rerank_model: str = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',
                 generation_model: str = "gemini-2.5-flash",
                 collection_name: str = "default",
                 persist_directory: Optional[str] = None):
        """初始化RAG系统
        
        Args:
            embedding_model: 嵌入模型名称
            rerank_model: 重排序模型名称
            generation_model: 生成模型名称
            collection_name: 向量存储集合名称
            persist_directory: 向量存储持久化目录
        """
        self.doc_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService(embedding_model)
        self.vector_store = VectorStore(collection_name, persist_directory)
        self.reranker = Reranker(rerank_model)
        self.generator = Generator(generation_model)
    
    def load_document(self, doc_file: str) -> int:
        """加载文档到系统
        
        Args:
            doc_file: 文档文件路径
            
        Returns:
            加载的文档块数量
        """
        # 分割文档
        chunks = self.doc_processor.split_into_chunks(doc_file)
        
        # 生成嵌入
        embeddings = self.embedding_service.embed_batch(chunks)
        
        # 存储到向量数据库
        self.vector_store.add_documents(chunks, embeddings)
        
        return len(chunks)
    
    def query(self, question: str, 
              retrieve_k: int = 5, 
              rerank_k: int = 3,
              show_prompt: bool = False) -> str:
        """查询系统并生成回答
        
        Args:
            question: 用户问题
            retrieve_k: 检索的文档数量
            rerank_k: 重排序后保留的文档数量
            show_prompt: 是否显示生成提示词
            
        Returns:
            生成的回答
        """
        # 1. 检索相关文档
        retrieved_chunks = self.retrieve(question, retrieve_k)
        
        # 2. 重排序
        reranked_chunks = self.reranker.rerank(question, retrieved_chunks, rerank_k)
        
        # 3. 生成回答
        answer = self.generator.generate_answer(question, reranked_chunks, show_prompt)
        
        return answer
    
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """检索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回的文档数量
            
        Returns:
            检索到的文档列表
        """
        query_embedding = self.embedding_service.embed_text(query)
        results = self.vector_store.search(query_embedding, top_k)
        return results['documents'][0] if results['documents'] else []
    
    def get_system_info(self) -> dict:
        """获取系统信息
        
        Returns:
            系统信息字典
        """
        return {
            "embedding_service": self.embedding_service.get_model_info(),
            "reranker": self.reranker.get_model_info(),
            "generator": self.generator.get_model_info(),
            "document_count": self.vector_store.count()
        }
    
    def clear_documents(self) -> None:
        """清空所有文档"""
        self.vector_store.clear()
    
    def add_documents_from_texts(self, texts: List[str]) -> int:
        """从文本列表添加文档
        
        Args:
            texts: 文本列表
            
        Returns:
            添加的文档数量
        """
        embeddings = self.embedding_service.embed_batch(texts)
        self.vector_store.add_documents(texts, embeddings)
        return len(texts)