#!/usr/bin/env python3
"""
DeepSeek生成器使用示例

演示如何使用DeepSeekGenerator进行文本生成和RAG问答。

使用前请确保：
1. 设置环境变量 DEEPSEEK_API_KEY
2. 安装依赖：pip install requests python-dotenv
"""

import os
from services.generator import DeepSeekGenerator
from core.rag_system import RAGSystem


def test_deepseek_generator():
    """测试DeepSeek生成器基本功能"""
    print("=== DeepSeek生成器基本功能测试 ===")
    
    try:
        # 初始化DeepSeek生成器
        generator = DeepSeekGenerator()
        
        # 获取模型信息
        model_info = generator.get_model_info()
        print(f"模型信息: {model_info}")
        
        # 测试简单问答
        print("\n--- 简单问答测试 ---")
        response = generator.generate_with_custom_prompt("请简单介绍一下人工智能")
        print(f"回答: {response}")
        
        # 测试基于上下文的问答
        print("\n--- 基于上下文的问答测试 ---")
        context_chunks = [
            "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
            "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。",
            "深度学习是机器学习的一个分支，使用神经网络来模拟人脑的工作方式。"
        ]
        
        query = "什么是深度学习？"
        response = generator.generate_answer(query, context_chunks, show_prompt=True)
        print(f"回答: {response}")
        
        # 测试流式响应
        print("\n--- 流式响应测试 ---")
        print("流式回答: ", end="")
        stream_response = generator.generate_with_custom_prompt(
            "请用一句话解释什么是RAG系统", 
            stream=True
        )
        print(stream_response)
        
    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置 DEEPSEEK_API_KEY 环境变量")


def test_rag_with_deepseek():
    """测试RAG系统与DeepSeek生成器的集成"""
    print("\n\n=== RAG系统与DeepSeek集成测试 ===")
    
    try:
        # 创建自定义RAG系统，使用DeepSeek作为生成器
        deepseek_generator = DeepSeekGenerator()
        
        # 注意：这里需要手动替换RAGSystem中的生成器
        # 在实际使用中，可以修改RAGSystem类来支持自定义生成器
        print("提示：要完全集成DeepSeek到RAG系统，需要修改RAGSystem类")
        print("支持在初始化时传入自定义生成器参数")
        
        # 演示如何手动使用DeepSeek进行RAG流程
        print("\n--- 手动RAG流程演示 ---")
        
        # 模拟检索到的上下文
        retrieved_contexts = [
            "RAG（Retrieval-Augmented Generation）是一种结合了信息检索和文本生成的AI技术。",
            "RAG系统首先从知识库中检索相关信息，然后基于这些信息生成回答。",
            "这种方法可以提高生成内容的准确性和相关性。"
        ]
        
        user_query = "RAG系统的工作原理是什么？"
        
        # 使用DeepSeek生成器生成回答
        answer = deepseek_generator.generate_answer(
            user_query, 
            retrieved_contexts, 
            show_prompt=True
        )
        
        print(f"\n用户问题: {user_query}")
        print(f"RAG回答: {answer}")
        
    except Exception as e:
        print(f"错误: {e}")


def show_usage_examples():
    """显示使用示例"""
    print("\n\n=== DeepSeek生成器使用示例 ===")
    
    example_code = '''
# 1. 基本使用
from services.generator import DeepSeekGenerator

# 初始化（需要设置DEEPSEEK_API_KEY环境变量）
generator = DeepSeekGenerator()

# 简单问答
response = generator.generate_with_custom_prompt("你好，请介绍一下自己")
print(response)

# 2. 基于上下文的问答（RAG场景）
context_chunks = ["相关文档片段1", "相关文档片段2"]
query = "用户问题"
answer = generator.generate_answer(query, context_chunks)
print(answer)

# 3. 流式响应
stream_response = generator.generate_with_custom_prompt(
    "请详细解释机器学习", 
    stream=True
)
print(stream_response)

# 4. 自定义模型和API密钥
custom_generator = DeepSeekGenerator(
    model_name="deepseek-chat",
    api_key="your-api-key-here"
)
'''
    
    print(example_code)


if __name__ == "__main__":
    # 检查API密钥
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("警告: 未设置 DEEPSEEK_API_KEY 环境变量")
        print("请设置后再运行测试")
        print("\n设置方法:")
        print("export DEEPSEEK_API_KEY='your-api-key-here'")
        print("或在 .env 文件中添加: DEEPSEEK_API_KEY=your-api-key-here")
        show_usage_examples()
    else:
        # 运行测试
        test_deepseek_generator()
        test_rag_with_deepseek()
        show_usage_examples()