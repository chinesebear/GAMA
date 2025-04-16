from src.Agents.API_info import ChatActionRunner

class ChatService:
    def __init__(self):
        self.runner = ChatActionRunner()

    async def get_response(self, messages: list) -> str:
        return await self.runner.execute(messages)
