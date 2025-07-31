#!/usr/bin/env python3
"""
测试DeepSeek生成器的导入和基本功能

这个脚本用于验证DeepSeekGenerator是否能正确导入和初始化。
"""

import os

def test_deepseek_import():
    """测试DeepSeek生成器的导入"""
    print("=== 测试DeepSeek生成器导入 ===")
    
    try:
        # 测试从services子包导入
        from services.generator import DeepSeekGenerator
        print("✓ 从services.generator导入DeepSeekGenerator成功")
        
        # 测试从顶层包导入
        from services import DeepSeekGenerator as DeepSeekGen
        print("✓ 从services包导入DeepSeekGenerator成功")
        
        # 测试从主包导入（如果在包内运行）
        try:
            import sys
            sys.path.insert(0, '..')
            from __init__ import DeepSeekGenerator as MainDeepSeek
            print("✓ 从主包导入DeepSeekGenerator成功")
        except ImportError:
            print("- 主包导入测试跳过（正常，因为不在包环境中）")
        
        return DeepSeekGenerator
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return None

def test_deepseek_initialization():
    """测试DeepSeek生成器的初始化"""
    print("\n=== 测试DeepSeek生成器初始化 ===")
    
    try:
        from services.generator import DeepSeekGenerator
        
        # 测试无API密钥的情况
        print("测试无API密钥初始化...")
        old_key = os.environ.get('DEEPSEEK_API_KEY')
        if 'DEEPSEEK_API_KEY' in os.environ:
            del os.environ['DEEPSEEK_API_KEY']
        
        try:
            generator = DeepSeekGenerator()
            print("✗ 应该抛出ValueError但没有")
        except ValueError as e:
            print(f"✓ 正确抛出ValueError: {e}")
        except Exception as e:
            print(f"✗ 抛出了意外的异常: {e}")
        
        # 恢复API密钥
        if old_key:
            os.environ['DEEPSEEK_API_KEY'] = old_key
        
        # 测试使用参数提供API密钥
        print("\n测试使用参数提供API密钥...")
        try:
            generator = DeepSeekGenerator(api_key="test-key")
            print("✓ 使用参数API密钥初始化成功")
            
            # 测试获取模型信息
            model_info = generator.get_model_info()
            print(f"✓ 获取模型信息成功: {model_info}")
            
        except Exception as e:
            print(f"✗ 初始化失败: {e}")
        
        # 测试自定义模型名称
        print("\n测试自定义模型名称...")
        try:
            custom_generator = DeepSeekGenerator(
                model_name="deepseek-coder", 
                api_key="test-key"
            )
            info = custom_generator.get_model_info()
            print(f"✓ 自定义模型初始化成功: {info}")
            
        except Exception as e:
            print(f"✗ 自定义模型初始化失败: {e}")
            
    except Exception as e:
        print(f"✗ 测试过程中出现错误: {e}")

def test_deepseek_methods():
    """测试DeepSeek生成器的方法"""
    print("\n=== 测试DeepSeek生成器方法 ===")
    
    try:
        from services.generator import DeepSeekGenerator
        
        # 创建测试实例
        generator = DeepSeekGenerator(api_key="test-key")
        
        # 测试_build_prompt方法
        print("测试_build_prompt方法...")
        query = "什么是人工智能？"
        context_chunks = ["AI是计算机科学的分支", "机器学习是AI的子集"]
        prompt = generator._build_prompt(query, context_chunks)
        print(f"✓ 构建提示词成功，长度: {len(prompt)}")
        
        # 测试方法存在性
        methods_to_test = [
            'generate_answer',
            'generate_with_custom_prompt', 
            '_call_api',
            '_handle_stream_response',
            'get_model_info'
        ]
        
        for method_name in methods_to_test:
            if hasattr(generator, method_name):
                print(f"✓ 方法 {method_name} 存在")
            else:
                print(f"✗ 方法 {method_name} 不存在")
        
        print("\n注意: 实际API调用需要有效的DEEPSEEK_API_KEY")
        
    except Exception as e:
        print(f"✗ 方法测试失败: {e}")

def show_usage_info():
    """显示使用信息"""
    print("\n=== DeepSeek生成器使用信息 ===")
    print("""
1. 设置API密钥:
   export DEEPSEEK_API_KEY='your-api-key-here'
   或在.env文件中添加: DEEPSEEK_API_KEY=your-api-key-here

2. 基本使用:
   from services.generator import DeepSeekGenerator
   generator = DeepSeekGenerator()
   response = generator.generate_with_custom_prompt("你好")

3. 在RAG系统中使用:
   # 可以替换默认的Generator
   # 或者手动使用DeepSeekGenerator处理检索到的上下文

4. 运行完整示例:
   python deepseek_example.py
""")

if __name__ == "__main__":
    print("DeepSeek生成器测试脚本")
    print("=" * 50)
    
    # 运行所有测试
    generator_class = test_deepseek_import()
    
    if generator_class:
        test_deepseek_initialization()
        test_deepseek_methods()
    
    show_usage_info()
    
    print("\n测试完成！")