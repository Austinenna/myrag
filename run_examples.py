#!/usr/bin/env python3
"""运行示例脚本的入口文件"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.reranker import Reranker
from services.generator import Generator


def example_individual_modules():
    """演示如何单独使用各个模块"""
    print("=== 演示各个模块的独立使用 ===")
    
    # 1. 文档处理
    print("\n1. 文档处理模块")
    doc_processor = DocumentProcessor()
    chunks = doc_processor.split_into_chunks("doc.md")
    print(f"文档分割成 {len(chunks)} 个块")
    print(f"第一个块: {chunks[0][:100]}...")
    
    # 2. 嵌入服务
    print("\n2. 嵌入服务模块")
    embedding_service = EmbeddingService()
    embedding = embedding_service.embed_text("测试文本")
    print(f"嵌入向量维度: {len(embedding)}")
    print(f"模型信息: {embedding_service.get_model_info()}")
    
    # 3. 向量存储
    print("\n3. 向量存储模块")
    vector_store = VectorStore("test_collection")
    
    # 批量生成嵌入
    embeddings = embedding_service.embed_batch(chunks[:3])  # 只处理前3个块作为示例
    
    # 存储文档
    vector_store.add_documents(chunks[:3], embeddings)
    print(f"存储了 {vector_store.count()} 个文档")
    
    # 搜索
    query = "哆啦A梦的道具"
    query_embedding = embedding_service.embed_text(query)
    search_results = vector_store.search(query_embedding, top_k=2)
    print(f"搜索结果: {len(search_results['documents'][0])} 个文档")
    
    # 4. 重排序
    print("\n4. 重排序模块")
    reranker = Reranker()
    retrieved_docs = search_results['documents'][0]
    reranked_docs = reranker.rerank(query, retrieved_docs, top_k=2)
    print(f"重排序后文档数量: {len(reranked_docs)}")
    print(f"重排序模型信息: {reranker.get_model_info()}")
    
    # 5. 生成器
    print("\n5. 生成器模块")
    generator = Generator()
    answer = generator.generate_answer(query, reranked_docs, show_prompt=False)
    print(f"生成的回答: {answer[:200]}...")
    print(f"生成器信息: {generator.get_model_info()}")
    
    # 清理
    vector_store.clear()
    print("\n清理完成")


def example_custom_workflow():
    """演示自定义工作流程"""
    print("\n\n=== 演示自定义工作流程 ===")
    
    # 创建组件
    doc_processor = DocumentProcessor()
    embedding_service = EmbeddingService()
    vector_store = VectorStore("custom_workflow")
    reranker = Reranker()
    generator = Generator()
    
    # 自定义文档处理
    print("\n1. 自定义文档处理")
    text = "这是一个测试文档。它包含多个句子。每个句子都很重要。我们需要将它们分割。"
    custom_chunks = doc_processor.split_by_sentences(text, max_length=20)
    print(f"按句子分割: {custom_chunks}")
    
    # 处理自定义文本
    print("\n2. 处理自定义文本")
    custom_texts = [
        "哆啦A梦是一只来自未来的机器猫。",
        "他有一个四次元口袋，里面有很多神奇的道具。",
        "竹蜻蜓可以让人飞行。",
        "任意门可以瞬间移动到任何地方。"
    ]
    
    embeddings = embedding_service.embed_batch(custom_texts)
    vector_store.add_documents(custom_texts, embeddings)
    
    # 查询和生成
    query = "哆啦A梦有什么道具？"
    query_embedding = embedding_service.embed_text(query)
    results = vector_store.search(query_embedding, top_k=3)
    
    reranked = reranker.rerank_with_scores(query, results['documents'][0], top_k=2)
    print(f"\n3. 重排序结果（带分数）:")
    for doc, score in reranked:
        print(f"分数: {score:.4f}, 文档: {doc}")
    
    # 生成回答
    final_docs = [doc for doc, _ in reranked]
    answer = generator.generate_answer(query, final_docs)
    print(f"\n4. 最终回答: {answer}")
    
    # 清理
    vector_store.clear()


if __name__ == "__main__":
    example_individual_modules()
    example_custom_workflow()