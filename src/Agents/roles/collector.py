from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio

class QuestionCollector:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.Segmentation = Columbus.Segmentation

    async def collect(self, question):
        try:
            all_content = self.Segmentation.format(question=question)
            print("------------------------------------collect_information----------------------------------------")

            # 并行执行多个异步操作
            related_message =await self.runner.execute(all_content)
            print("------------------------------------collect_end----------------------------------------")
            return related_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
