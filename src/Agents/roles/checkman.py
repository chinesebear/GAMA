from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio



class CheckMan:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.repairman = Columbus.repairman

    async def repair(self, question,all_answer):
        try:
            all_content = self.repairman.format(Question=question,answer=all_answer)
            print("------------------------------------repair_person----------------------------------------")

            # 并行执行多个异步操作
            finally_answer = await self.runner.execute(all_content)
            print("------------------------------------repair_end----------------------------------------")
            return finally_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


