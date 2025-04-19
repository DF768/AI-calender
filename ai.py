import requests
import json
from openai import OpenAI

class AIClient:
    def __init__(self, base_url="http://127.0.0.1:11434/v1"):
        self.base_url = base_url 
    def GetOpenai(self, base_url="http://127.0.0.1:11434/v1"):
        # 初始化客户端
        client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="lm-studio")
        self.base_url = client
        # 调用API生成对话
        completion = client.chat.completions.create(
            model="deepseek-r1:1.5b",  # 使用的模型
            messages=[
                #{"role": "system", "content": "你是一个专业的助手，回答问题时必须准确，且不能胡言乱语。"},  # 系统提示
                {"role": "user", "content": "你好，你叫什么名字"}  # 用户输入
            ],
            temperature=0.7,  # 控制输出的随机性，值越低输出越确定
            top_p=0.9,        # 控制输出的多样性，值越低输出越集中
            max_tokens=512,   # 控制生成的最大token数量
            frequency_penalty=0.5,  # 减少重复内容的生成
            presence_penalty=0.5    # 鼓励模型引入新内容
        )
 
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
        
        response = requests.post(
            self.base_url,
            json={
                "model": "deepseek",
                "prompt": prompt,
                "system": system_prompt,
                "format": "json",
                "stream": False
            }
        )
        
        try:
            return json.loads(response.text)["response"]
        except:
            return None
        






        