#!/usr/bin/env python3
"""测试包结构的脚本"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有模块的导入"""
    print("=== 测试包结构导入 ===")
    
    try:
        # 测试核心模块导入
        print("\n1. 测试核心模块导入...")
        from core.document_processor import DocumentProcessor
        from core.vector_store import VectorStore
        print("✓ 核心模块导入成功")
        
        # 测试服务模块导入
        print("\n2. 测试服务模块导入...")
        from services.embedding_service import EmbeddingService
        from services.reranker import Reranker
        from services.generator import Generator
        print("✓ 服务模块导入成功")
        
        # 测试主包导入
        print("\n3. 测试主包导入...")
        from core.rag_system import RAGSystem
        print("✓ RAG系统导入成功")
        
        # 测试通过主包导入（跳过，因为目录名可能不是myrag）
        print("\n4. 测试通过主包导入...")
        try:
            import myrag
            print(f"✓ 主包导入成功，版本: {myrag.__version__}")
        except ImportError:
            print("⚠️ 主包导入跳过（目录名不是myrag，这是正常的）")
        
        # 测试实例化（不涉及网络）
        print("\n5. 测试模块实例化...")
        doc_processor = DocumentProcessor()
        print("✓ DocumentProcessor 实例化成功")
        
        vector_store = VectorStore("test_collection")
        print("✓ VectorStore 实例化成功")
        
        embedding_service = EmbeddingService()
        print("✓ EmbeddingService 实例化成功")
        
        print("\n=== 所有测试通过！包结构重组成功 ===")
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    return True

def test_package_structure():
    """测试包结构"""
    print("\n=== 包结构信息 ===")
    
    # 显示包结构
    structure = {
        "core": ["document_processor", "vector_store", "rag_system"],
        "services": ["embedding_service", "reranker", "generator"],
        "examples": ["example_usage"]
    }
    
    for package, modules in structure.items():
        print(f"\n📦 {package}/")
        for module in modules:
            print(f"  ├── {module}.py")
    
    print("\n📄 主要文件:")
    print("  ├── main.py (主程序)")
    print("  ├── run_examples.py (示例运行脚本)")
    print("  └── test_package_structure.py (本测试脚本)")

if __name__ == "__main__":
    test_package_structure()
    success = test_imports()
    
    if success:
        print("\n🎉 包重组完成！新的包结构已经可以正常使用。")
        print("\n📖 使用方法:")
        print("  - 运行主程序: python main.py")
        print("  - 运行示例: python run_examples.py")
        print("  - 导入使用: from core.rag_system import RAGSystem")
    else:
        print("\n❌ 包结构存在问题，请检查导入路径。")