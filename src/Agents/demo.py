from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio



class CheckMan:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.repairman = '''
        You are an expert in Entertainment with an Extremely High level of expertise.
        Answer this question：question 5: What was Eddie Murphy's first movie?
        The answer should be as comprehensive as possible and should not exceed 20 words.Check before replying.
        Use formal language.
        Do not use abbreviations when replying to movie names, people names, or place names.'''

    async def repair(self, question,all_answer):
        try:
            print("------------------------------------repair_person----------------------------------------")

            # 并行执行多个异步操作
            finally_answer = await self.runner.execute(self.repairman)
            print("------------------------------------repair_end----------------------------------------")
            return finally_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

check_man = CheckMan()

# 异步执行 repair 方法
async def main():
    question = "aswdadas"
    all_answer = None  # 如果你有其他答案，可以传入
    result = await check_man.repair(question, all_answer)
    print(f"Final answer: {result}")

# 运行异步任务
asyncio.run(main())