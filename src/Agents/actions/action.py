import asyncio
from src.Agents.actions.action_output import chat_completion_to_dict
class Action:
    def __init__(self, chat_client):
        self.chat_client = chat_client


    async def run(self, user_input, model):
        loop = asyncio.get_running_loop()
        # 使用 run_in_executor 允许在异步函数中调用同步方法
        response = await loop.run_in_executor(None, self.chat_client.fetch_chat_response, user_input, model)
        return chat_completion_to_dict(response)




