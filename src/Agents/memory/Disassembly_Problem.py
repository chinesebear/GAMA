from src.Agents.API_info import ChatActionRunner
from src.Agents.memory.key_memory import *
import asyncio



class DisassemblyProblem:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.Disassembly = Disassembly

    async def disassembly(self, questions):
        try:

            print("------------------------------------Disassembly---------------------------------------")
            all_content = self.Disassembly.format(Questions=questions)
            # 并行执行多个异步操作
            finally_answer = await self.runner.execute(all_content)
            print(finally_answer)

            print("------------------------------------Disassembly_end----------------------------------------")

            return finally_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None