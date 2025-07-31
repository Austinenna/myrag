from services.generator import DeepSeekGenerator

# 需要设置环境变量 DEEPSEEK_API_KEY
generator = DeepSeekGenerator()
response = generator.generate_with_custom_prompt("你好")

print(response)