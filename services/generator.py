from typing import List
import os
import json
import requests
from dotenv import load_dotenv
from google import genai


class Generator:
    """生成器，负责基于检索到的内容生成回答"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """初始化生成器
        
        Args:
            model_name: 生成模型名称
        """
        load_dotenv()
        self.model_name = model_name
        self.client = genai.Client()
    
    def generate_answer(self, query: str, context_chunks: List[str], 
                       show_prompt: bool = False) -> str:
        """基于查询和上下文生成回答
        
        Args:
            query: 用户查询
            context_chunks: 相关的上下文片段
            show_prompt: 是否显示提示词
            
        Returns:
            生成的回答
        """
        prompt = self._build_prompt(query, context_chunks)
        
        if show_prompt:
            print(f"{prompt}\n\n---\n")
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        return response.text
    
    def _build_prompt(self, query: str, context_chunks: List[str]) -> str:
        """构建提示词
        
        Args:
            query: 用户查询
            context_chunks: 上下文片段
            
        Returns:
            构建的提示词
        """
        context = "\n\n".join(context_chunks)
        
        prompt = f"""你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。

用户问题: {query}

相关片段:
{context}

请基于上述内容作答，不要编造信息。"""
        
        return prompt
    
    def generate_with_custom_prompt(self, custom_prompt: str) -> str:
        """使用自定义提示词生成回答
        
        Args:
            custom_prompt: 自定义提示词
            
        Returns:
            生成的回答
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=custom_prompt
        )
        
        return response.text
    
    def get_model_info(self) -> dict:
        """获取模型信息
        
        Returns:
            模型信息字典
        """
        return {
            "model_name": self.model_name,
            "provider": "Google Gemini"
        }


class DeepSeekGenerator:
    """DeepSeek生成器，基于DeepSeek API生成回答"""
    
    def __init__(self, model_name: str = "deepseek-chat", api_key: str = None):
        """初始化DeepSeek生成器
        
        Args:
            model_name: DeepSeek模型名称
            api_key: API密钥，如果不提供则从环境变量DEEPSEEK_API_KEY获取
        """
        load_dotenv()
        self.model_name = model_name
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("请设置环境变量 DEEPSEEK_API_KEY 或提供 api_key 参数")
    
    def generate_answer(self, query: str, context_chunks: List[str], 
                       show_prompt: bool = False, stream: bool = False) -> str:
        """基于查询和上下文生成回答
        
        Args:
            query: 用户查询
            context_chunks: 相关的上下文片段
            show_prompt: 是否显示提示词
            stream: 是否使用流式响应
            
        Returns:
            生成的回答
        """
        prompt = self._build_prompt(query, context_chunks)
        
        if show_prompt:
            print(f"{prompt}\n\n---\n")
        
        return self._call_api(prompt, stream=stream)
    
    def _build_prompt(self, query: str, context_chunks: List[str]) -> str:
        """构建提示词
        
        Args:
            query: 用户查询
            context_chunks: 上下文片段
            
        Returns:
            构建的提示词
        """
        context = "\n\n".join(context_chunks)
        
        prompt = f"""你是一位知识助手，请根据用户的问题和下列片段生成准确的回答。

用户问题: {query}

相关片段:
{context}

请基于上述内容作答，不要编造信息。"""
        
        return prompt
    
    def generate_with_custom_prompt(self, custom_prompt: str, stream: bool = False) -> str:
        """使用自定义提示词生成回答
        
        Args:
            custom_prompt: 自定义提示词
            stream: 是否使用流式响应
            
        Returns:
            生成的回答
        """
        return self._call_api(custom_prompt, stream=stream)
    
    def _call_api(self, prompt: str, stream: bool = False) -> str:
        """调用DeepSeek API
        
        Args:
            prompt: 提示词
            stream: 是否使用流式响应
            
        Returns:
            生成的回答
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 系统提示词
        system_prompt = "你是一个有用的AI助手，请用简洁明了的方式回答问题。"
        
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data, 
                timeout=30, 
                stream=stream
            )
            
            if response.status_code == 200:
                if stream:
                    return self._handle_stream_response(response)
                else:
                    result = response.json()
                    return result['choices'][0]['message']['content']
            else:
                error_msg = f"API调用失败: HTTP {response.status_code}"
                try:
                    error_info = response.json()
                    error_msg += f" - {error_info.get('error', {}).get('message', '未知错误')}"
                except:
                    error_msg += f" - {response.text}"
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            raise Exception("网络连接失败，请检查网络设置")
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常: {e}")
        except Exception as e:
            if "API调用失败" in str(e):
                raise
            raise Exception(f"未知错误: {e}")
    
    def _handle_stream_response(self, response) -> str:
        """处理流式响应
        
        Args:
            response: requests响应对象
            
        Returns:
            完整的回答内容
        """
        content = ""
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    line = line[6:]  # 移除 'data: ' 前缀
                    
                    if line.strip() == '[DONE]':
                        break
                    
                    try:
                        chunk = json.loads(line)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                content += delta['content']
                    except json.JSONDecodeError:
                        continue
        
        return content
    
    def get_model_info(self) -> dict:
        """获取模型信息
        
        Returns:
            模型信息字典
        """
        return {
            "model_name": self.model_name,
            "provider": "DeepSeek",
            "api_url": self.api_url
        }