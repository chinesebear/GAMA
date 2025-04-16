from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
from src.Agents.roles.logic_math import *
import asyncio
import re


class PlanerLogic:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.math_logic = math_logic
        self.spp_plus = spp_prompt
        self.check_logic = check_logic
        self.pattern = r"//(.+?)//"
        self.c_prompt =cond_prompt
        self.think_again=think_again
    async def logic(self, question):
        try:
            all_content = self.math_logic.format(question=question)
            print("\033[1;32m------------------------------------ LOGIC THINKING ----------------------------------------\033[0m")

            # 并行执行多个异步操作

            related_message = await self.runner.execute(all_content)
            print("Answer:",related_message)
            print("\033[1;32m------------------------------------ THINK_END ----------------------------------------\033[0m")
            return related_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def analyze_text(self, text):  # 修改这里，去掉async
        matches = re.findall(self.pattern, text, re.IGNORECASE)
        combined_sentence = ' '.join(matches).lower()
        if "correct" in combined_sentence:
            return True
        elif "wrong" in combined_sentence:
            return False
        return True


    async def condense(self, question,answer,related_message):
        try:
            all_content = self.c_prompt.format(question=question,answer=answer,condence=related_message)
            print("\033[1;32m------------------------------------ CONDENSE_CONTRADICTION ----------------------------------------\033[0m")
            # 并行执行多个异步操作
            cond_info = await self.runner.execute(all_content)

            print("Briefly describe the contradiction:",cond_info)
            print("\033[1;32m------------------------------------ CONDENSE_END ----------------------------------------\033[0m")

            return cond_info
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    async def verify(self, question, answer):
        try:
            all_content = self.check_logic.format(question=question, solutions=answer)
            print("\033[1;32m------------------------------------ VERIFY_THINKING ----------------------------------------\033[0m")

            # 并行执行多个异步操作
            related_message = await self.runner.execute(all_content)
            print("VERIFY_THINK_RESULT:",related_message)
            print("------------------------------------THINKING_END-------------------------------------------")

            contradiction = self.analyze_text(
                related_message)
            contradiction_info ='no contradiction_info'
            if not contradiction:
                print("☆☆☆☆☆☆☆☆☆☆☆The answer obtained this time was evaluated to be wrong☆☆☆☆☆☆☆☆☆☆☆")
                contradiction_info = await self.condense(question,answer,related_message)

            return contradiction,contradiction_info
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    async def logic_again(self, question,answer,memory):
        try:
            all_content = self.think_again.format(question=question,answer=answer,memory=memory)
            print("\033[1;32m------------------------------------ LOGIC_THINKING_AGAIN ----------------------------------------\033[0m")

            # 并行执行多个异步操作

            related_message = await self.runner.execute(all_content)
            print("THINK AGAIN",related_message)
            print("\033[1;32m------------------------------------ THINKING_END ----------------------------------------\033[0m")

            return related_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

