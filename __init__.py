"""MyRAG - 模块化检索增强生成系统

这是一个模块化的RAG（Retrieval-Augmented Generation）系统，
包含文档处理、嵌入、向量存储、重排序和生成等功能模块。

包结构：
- core: 核心功能模块（文档处理、向量存储、RAG系统）
- services: 服务层模块（嵌入、重排序、生成服务）
- examples: 示例和演示模块
"""

# 从子包导入主要类
from .core import DocumentProcessor, VectorStore, RAGSystem
from .services import EmbeddingService, Reranker, Generator, DeepSeekGenerator

__version__ = "1.0.0"
__author__ = "MyRAG Team"
__email__ = "contact@myrag.com"

__all__ = [
    'DocumentProcessor',
    'EmbeddingService',
    'VectorStore',
    'Reranker',
    'Generator',
    'DeepSeekGenerator',
    'RAGSystem'
]