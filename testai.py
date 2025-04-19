import requests
import json
from openai import OpenAI


class AIClient:
    def __init__(self, base_url="http://127.0.0.1:11434/v1"):
        self.base_url = base_url + "/api/generate"
    
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

    def get_openai_response(self, model, messages, temperature=0.7, top_p=0.9, max_tokens=512, frequency_penalty=0.5, presence_penalty=0.5):
        # 初始化客户端
        client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="lm-studio")
 
        # 调用API生成对话
        completion = client.chat.completions.create(
            model=model,  # 使用的模型
            messages=messages,
            temperature=temperature,  # 控制输出的随机性，值越低输出越确定
            top_p=top_p,        # 控制输出的多样性，值越低输出越集中
            max_tokens=max_tokens,   # 控制生成的最大token数量
            frequency_penalty=frequency_penalty,  # 减少重复内容的生成
            presence_penalty=presence_penalty    # 鼓励模型引入新内容
        )
 
        # 返回生成的回复
        return completion.choices[0].message.content


if __name__ == '__main__':
    ai_client = AIClient()
    # 测试 generate_plan 方法
    plan = ai_client.generate_plan("请为我安排一个明天下午3点到5点的会议，主题是项目讨论，地点在公司会议室，需要包括技术团队和市场团队的成员。")
    print("生成的日历事件计划：")
    print(plan)
    
    # 测试 get_openai_response 方法
    response = ai_client.get_openai_response(
        model="deepseek-r1:1.5b",
        messages=[
            {"role": "user", "content": "请为我安排一个明天下午3点到5点的会议，主题是项目讨论，地点在公司会议室，需要包括技术团队和市场团队的成员。"}
        ]
    )
    print("\n生成的对话回复：")
    print(response)