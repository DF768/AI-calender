import json
from typing import Optional, Dict
from openai import OpenAI
from PyQt5.QtCore import QDate, QTime, QDateTime
# from PyQt5.QtWidgets import QMessageBox
#适用PyQt5的QMessageBox来显示错误信息
from ..logged.config import config
from ..logged.og import logger

class AIClient:
    def __init__(self):
        self.client = OpenAI(
            base_url=config.API_BASE_URL,
            api_key=config.API_KEY
        )
        self.model = config.MODEL_NAME

    def generate_plan(
        self, 
        user_input: str, 
        selected_date: QDate
    ) -> Optional[Dict[str, str]]:
        """使用AI生成日历计划"""
        try:
            time_data = selected_date.toString("yyyy-MM-dd")
            system_prompt = self._build_system_prompt(time_data)
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                max_tokens=512,
                top_p=0.9,
                response_format={"type": "json_object"}
            )

            response_text = completion.choices[0].message.content
            return self._parse_response(response_text, selected_date)
            
        except Exception as e:
            logger.error(f"AI API Error: {e}", exc_info=True)
            return None

    def _build_system_prompt(self, current_date: str) -> str:
        """构建系统提示词"""
        return f"""当前日期是{current_date}，用户将输入包含时间和事件的描述，你需要：
1. 识别所有时间相关表达（绝对时间、相对时间和周期时间）
2. 自动转换时间为具体日期和时间（格式：YYYY-MM-DD HH:mm）
3. 按以下JSON格式返回结果：
{{
    "title": "事件标题",
    "date": "计算后的日期（YYYY-MM-DD）",
    "time": "具体时间（HH:mm或全天）",
    "duration": 默认1小时（单位：分钟）
}}"""

    def _parse_response(
        self, 
        response_text: str, 
        base_date: QDate
    ) -> Optional[Dict[str, str]]:
        """解析AI响应"""
        try:
            data = json.loads(response_text)
            
            event_date = QDate.fromString(data["date"], "yyyy-MM-dd")
            if not event_date.isValid():
                logger.warning(f"Invalid date format: {data['date']}")
                return None

            if data["time"] == "全天":
                start_time = QTime(0, 0)
                end_time = QTime(23, 59)
            else:
                start_time = QTime.fromString(data["time"], "HH:mm")
                if not start_time.isValid():
                    logger.warning(f"Invalid time format: {data['time']}")
                    return None
                
                duration = data.get("duration", 60)
                end_time = start_time.addSecs(duration * 60)

            return {
                "title": data["title"],
                "start": QDateTime(event_date, start_time).toString("yyyy-MM-dd HH:mm:ss"),
                "end": QDateTime(event_date, end_time).toString("yyyy-MM-dd HH:mm:ss")
            }
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Response parsing failed: {e}", exc_info=True)
            return None