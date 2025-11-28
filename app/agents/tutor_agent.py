import asyncio
from datetime import datetime

class TutorAgent:
    def __init__(self):
        self.conversation_history = []

    async def process_user_message(self, message: str, code_context: dict):
        """处理用户消息 - Python 3.9 兼容版本"""

        # 记录对话历史
        self.conversation_history.append({
            'role': 'user',
            'content': message,
            'code_context': code_context
        })

        # 生成响应
        response = await self._generate_guided_response(message, code_context)

        self.conversation_history.append({
            'role': 'assistant', 
            'content': response
        })

        return {
            "type": "response",
            "content": response,
            "timestamp": self._get_timestamp()
        }

    async def _generate_guided_response(self, message: str, code_context: dict) -> str:
        """生成引导式回复"""
        if "错误" in message or "error" in message.lower():
            return "你遇到了错误？可以把错误信息发给我，或者直接上传代码，我来帮你分析。"
        elif "指针" in message:
            return "指针是C语言的难点。你能具体描述一下遇到的问题吗？比如是空指针、野指针还是内存分配问题？"
        elif "循环" in message or "loop" in message.lower():
            return "循环问题很常见。是无限循环、条件错误，还是循环变量的作用域问题？"
        else:
            return f"我收到了你的消息：'{message}'。让我们一步步来分析，你能先告诉我你期望程序实现什么功能吗？"

    def _get_timestamp(self):
        return datetime.now().isoformat()
