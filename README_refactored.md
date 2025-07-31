# MyRAG - 模块化检索增强生成系统

这是一个重构后的模块化RAG（Retrieval-Augmented Generation）系统，将原本的单文件代码拆分为多个独立的模块，提高了代码的可维护性、可重用性和可扩展性。

## 项目结构

```
myrag/
├── __init__.py                 # 包初始化文件
├── core/                       # 核心功能包
│   ├── __init__.py
│   ├── document_processor.py   # 文档处理模块
│   ├── vector_store.py        # 向量存储模块
│   └── rag_system.py          # RAG系统主类
├── services/                   # 服务层包
│   ├── __init__.py
│   ├── embedding_service.py    # 嵌入服务模块
│   ├── reranker.py            # 重排序模块
│   └── generator.py           # 生成模块
├── examples/                   # 示例包
│   ├── __init__.py
│   └── example_usage.py       # 使用示例
├── main.py                    # 主程序（重构后）
├── run_examples.py            # 示例运行脚本
└── README_refactored.md       # 本文件
```

## 模块说明

### 1. DocumentProcessor (文档处理器)
- **功能**: 负责文档的分块处理
- **主要方法**:
  - `split_into_chunks()`: 按段落分割文档
  - `split_by_sentences()`: 按句子分割文本，支持长度控制

### 2. EmbeddingService (嵌入服务)
- **功能**: 负责文本的向量化处理
- **主要方法**:
  - `embed_text()`: 单个文本嵌入
  - `embed_batch()`: 批量文本嵌入
  - `get_model_info()`: 获取模型信息

### 3. VectorStore (向量存储)
- **功能**: 负责向量的存储和检索
- **主要方法**:
  - `add_documents()`: 添加文档和嵌入
  - `search()`: 搜索相似文档
  - `clear()`: 清空存储
  - `count()`: 获取文档数量

### 4. Reranker (重排序器)
- **功能**: 对检索结果进行重新排序
- **主要方法**:
  - `rerank()`: 重排序文档
  - `rerank_with_scores()`: 重排序并返回分数
  - `get_model_info()`: 获取模型信息

### 5. Generator (生成器)
- **功能**: 基于检索到的内容生成回答
- **支持的生成器**:
  - `Generator`: 基于Google Gemini的生成器
  - `DeepSeekGenerator`: 基于DeepSeek API的生成器
- **主要方法**:
  - `generate_answer()`: 生成回答
  - `generate_with_custom_prompt()`: 使用自定义提示词生成
  - `get_model_info()`: 获取模型信息
- **DeepSeek特有功能**:
  - 支持流式响应
  - 自定义API密钥配置
  - 多种DeepSeek模型支持

### 6. RAGSystem (RAG系统主类)
- **功能**: 整合所有模块，提供统一的接口
- **主要方法**:
  - `load_document()`: 加载文档
  - `query()`: 查询并生成回答
  - `retrieve()`: 检索相关文档
  - `get_system_info()`: 获取系统信息

## 使用方法

### 1. 简单使用（推荐）

```python
from core.rag_system import RAGSystem

# 初始化系统
rag = RAGSystem()

# 加载文档
rag.load_document("your_document.md")

# 查询
answer = rag.query("你的问题")
print(answer)
```

### 2. 自定义配置

```python
from core.rag_system import RAGSystem

# 自定义模型配置
rag = RAGSystem(
    embedding_model="your-embedding-model",
    rerank_model="your-rerank-model",
    generation_model="your-generation-model",
    persist_directory="./vector_db"  # 持久化存储
)
```

### 3. 使用独立模块

```python
from core.document_processor import DocumentProcessor
from core.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.reranker import Reranker
from services.generator import Generator, DeepSeekGenerator

# 独立使用各个模块
doc_processor = DocumentProcessor()
embedding_service = EmbeddingService()
vector_store = VectorStore()

# 自定义工作流程
chunks = doc_processor.split_into_chunks("doc.md")
embeddings = embedding_service.embed_batch(chunks)
vector_store.add_documents(chunks, embeddings)
```

### 4. 使用DeepSeek生成器

```python
from services.generator import DeepSeekGenerator

# 基本使用（需要设置DEEPSEEK_API_KEY环境变量）
deepseek_gen = DeepSeekGenerator()

# 或者直接提供API密钥
deepseek_gen = DeepSeekGenerator(api_key="your-deepseek-api-key")

# 简单问答
response = deepseek_gen.generate_with_custom_prompt("请介绍一下人工智能")
print(response)

# 基于上下文的RAG问答
context_chunks = ["相关文档片段1", "相关文档片段2"]
query = "用户问题"
answer = deepseek_gen.generate_answer(query, context_chunks)
print(answer)

# 流式响应
stream_response = deepseek_gen.generate_with_custom_prompt(
    "请详细解释机器学习", 
    stream=True
)
print(stream_response)

# 自定义模型
custom_gen = DeepSeekGenerator(
    model_name="deepseek-coder",  # 使用代码专用模型
    api_key="your-api-key"
)
```

## 运行示例

### 运行主程序
```bash
python main.py
```

### 运行使用示例
```bash
python run_examples.py
```

### 运行包内示例（需要在包目录外）
```bash
python -m myrag.examples.example_usage
```

### 运行DeepSeek生成器示例
```bash
# 测试DeepSeek生成器导入和基本功能
python test_deepseek.py

# 运行完整的DeepSeek示例（需要API密钥）
python deepseek_example.py
```

## 重构的优势

### 1. 模块化设计
- 每个模块职责单一，易于理解和维护
- 模块间低耦合，高内聚
- 便于单元测试

### 2. 可重用性
- 各个模块可以独立使用
- 支持自定义工作流程
- 易于集成到其他项目

### 3. 可扩展性
- 易于添加新的文档处理方法
- 支持不同的嵌入模型和生成模型
- 可以轻松替换向量存储后端

### 4. 可配置性
- 支持自定义模型配置
- 支持持久化存储
- 灵活的参数调整

### 5. 易于维护
- 代码结构清晰
- 错误定位更容易
- 功能修改影响范围小

## 依赖项

确保安装以下依赖：

```bash
pip install sentence-transformers
pip install chromadb
pip install python-dotenv
pip install google-generativeai
pip install requests  # DeepSeek生成器需要
```

## 环境配置

创建 `.env` 文件并配置必要的API密钥：

```
# Google Gemini API密钥（用于默认Generator）
GOOGLE_API_KEY=your_google_api_key

# DeepSeek API密钥（用于DeepSeekGenerator）
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### API密钥获取方式

1. **Google Gemini API**:
   - 访问 [Google AI Studio](https://aistudio.google.com/)
   - 创建API密钥

2. **DeepSeek API**:
   - 访问 [DeepSeek官网](https://www.deepseek.com/)
   - 注册账号并获取API密钥

## 注意事项

1. 首次运行时，模型会自动下载到缓存目录
2. 确保有足够的磁盘空间存储模型文件
3. 生成功能需要有效的API密钥：
   - Google Gemini: 需要 `GOOGLE_API_KEY`
   - DeepSeek: 需要 `DEEPSEEK_API_KEY`
4. 建议在生产环境中使用持久化存储
5. DeepSeek API调用需要稳定的网络连接
6. 不同生成器的响应格式和性能可能有差异
7. 流式响应功能仅在DeepSeekGenerator中可用

## 下一步改进

- [ ] 添加更多文档格式支持（PDF、Word等）
- [ ] 支持更多向量数据库后端
- [ ] 添加配置文件支持
- [ ] 实现异步处理
- [ ] 添加日志系统
- [ ] 实现缓存机制
- [ ] 添加性能监控
- [ ] 支持更多生成器（OpenAI、Claude等）
- [ ] 在RAGSystem中集成DeepSeekGenerator选项
- [ ] 添加生成器性能对比工具
- [ ] 实现生成器自动切换和负载均衡
- [ ] 添加流式响应的Web界面支持