from typing import List, Optional
import chromadb
from chromadb.api.models.Collection import Collection


class VectorStore:
    """向量存储，负责向量的存储和检索"""
    
    def __init__(self, collection_name: str = "default", persist_directory: Optional[str] = None):
        """初始化向量存储
        
        Args:
            collection_name: 集合名称
            persist_directory: 持久化目录，如果为None则使用内存存储
        """
        self.collection_name = collection_name
        
        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.EphemeralClient()
        
        self.collection: Collection = self.client.get_or_create_collection(name=collection_name)
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], 
                     metadata: Optional[List[dict]] = None) -> None:
        """添加文档到向量存储
        
        Args:
            documents: 文档列表
            embeddings: 对应的嵌入向量列表
            metadata: 可选的元数据列表
        """
        ids = [str(i) for i in range(len(documents))]
        
        # 如果集合不为空，需要生成新的ID
        existing_count = self.collection.count()
        if existing_count > 0:
            ids = [str(existing_count + i) for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadata
        )
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> dict:
        """搜索相似文档
        
        Args:
            query_embedding: 查询向量
            top_k: 返回的文档数量
            
        Returns:
            搜索结果字典
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
    
    def get_documents(self) -> List[str]:
        """获取所有文档
        
        Returns:
            文档列表
        """
        results = self.collection.get()
        return results['documents']
    
    def clear(self) -> None:
        """清空集合"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
    
    def count(self) -> int:
        """获取文档数量
        
        Returns:
            文档数量
        """
        return self.collection.count()