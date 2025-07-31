from typing import List


class DocumentProcessor:
    """文档处理器，负责文档的分块处理"""
    
    def __init__(self):
        pass
    
    def split_into_chunks(self, doc_file: str) -> List[str]:
        """将文档分割成块
        
        Args:
            doc_file: 文档文件路径
            
        Returns:
            文档块列表
        """
        with open(doc_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
        # return [chunk.strip() for chunk in content.split("\n") if chunk.strip()]

    def split_by_sentences(self, text: str, max_length: int = 500) -> List[str]:
        """按句子分割文本，控制每块的最大长度
        
        Args:
            text: 输入文本
            max_length: 每块的最大字符数
            
        Returns:
            文本块列表
        """
        sentences = text.split('。')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence + '。') <= max_length:
                current_chunk += sentence + '。'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + '。'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return [chunk for chunk in chunks if chunk]