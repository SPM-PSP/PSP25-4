import os
from openai import OpenAI

# 获取环境变量的值
deepseek_api_key = os.environ.get("DeepSeek API Key")

if deepseek_api_key is None:
    raise ValueError("环境变量 'DeepSeek_API_Key' 未设置")

client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

messages.append(response.choices[0].message)
print(f"Messages Round 1: {messages}")
