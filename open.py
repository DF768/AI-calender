# ai.py
import json
from openai import OpenAI
 
class AIClient:
    def __init__(self, base_url="http://127.0.0.1:11434/v1", api_key="lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
 
    def generate_plan(self, prompt):
        system_prompt = """你是一个智能日历助手，请用以下JSON格式回复：
{
  "title": "事件标题",
  "start": "YYYY-MM-DD HH:MM",
  "end": "YYYY-MM-DD HH:MM",
  "description": "详细描述",
  "location": "地点（可选）",
  "tags": ["标签1", "标签2"]
}"""

        completion = self.client.chat.completions.create(
            model="deepseek-r1:1.5b",
        messages=[
            {"role": "user", "content": "你好，你叫什么名字"}  # 用户输入
        ],
        temperature=0.7,  # 控制输出的随机性，值越低输出越确定
        top_p=0.9,        # 控制输出的多样性，值越低输出越集中
        max_tokens=512,   # 控制生成的最大token数量
        frequency_penalty=0.5,  # 减少重复内容的生成
        presence_penalty=0.5    # 鼓励模型引入新内容
    )
 
        try:
            response_text = completion.choices[0].message.content
            return json.loads(response_text)
        except:
            return None
 
