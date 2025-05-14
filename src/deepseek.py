import os
from openai import OpenAI

deepseek_api_key = os.environ.get("DeepSeek API Key")

if deepseek_api_key is None:
    raise ValueError("环境变量 'DeepSeek_API_Key' 未设置")

client = OpenAI(
    api_key=deepseek_api_key,
    base_url="https://api.deepseek.com/beta",
)

response = client.completions.create(
    model="deepseek-chat",
    prompt="春天来了，万物复苏，",
    suffix="鸟儿在枝头欢快地歌唱，花儿也竞相开放。",
    max_tokens=128
)
print(response.choices[0].text)
