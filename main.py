"""使用重构后的模块化RAG系统"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.rag_system import RAGSystem


def main():
    """主函数，演示RAG系统的使用"""
    # 初始化RAG系统
    rag = RAGSystem(
        embedding_model="shibing624/text2vec-base-chinese",
        rerank_model='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',
        generation_model="gemini-2.5-flash"
    )
    
    # 加载文档
    print("正在加载文档...")
    doc_count = rag.load_document("doc.md")
    print(f"已加载 {doc_count} 个文档块")
    
    # 查询问题
    query = "哆啦A梦使用的3个秘密道具分别是什么？"
    print(f"\n查询问题: {query}")
    
    # 生成回答
    print("\n正在生成回答...")
    answer = rag.query(
        question=query,
        retrieve_k=5,
        rerank_k=3,
        show_prompt=True
    )
    
    print(f"\n回答: {answer}")
    
    # 显示系统信息
    print("\n=== 系统信息 ===")
    system_info = rag.get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()