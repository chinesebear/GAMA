from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio

class ProblemClassification:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.cls = '''
        Consider the following text sample and its attributes. If the text is structured to involve reasoning through clues or indirect hints, respond with "no". If the question requires background knowledge to answer, respond with "yes.".
        Here are two examples. 
        For example, if you are asked who will be the president of the United States in 2010, the answer is Obama. 
        Obviously, the question does not contain the answer, and you need to obtain background knowledge. 
        In this case, you should answer yes. When the question is A is greater than B, B is greater than C, and you ask whether A is greater than C? 
        This involves reasoning, and does not require background knowledge, so you should answer no.
        question: {question}"
        Based on the description and the sample, determine the appropriate response and provide either "no" or "yes".'''
    async def repair(self, question):
        try:
            all_content = self.cls.format(question=question)
            print("\033[1;32m------------------------------------ GET knowledge ----------------------------------------\033[0m")

            yes_count = 0
            no_count = 0

            # 执行三次finally_answer
            for i in range(3):
                finally_answer = await self.runner.execute(all_content)
                print(f"☆☆☆☆☆ Classification result {i+1}: {finally_answer}")

                # 统计yes和no的出现次数
                if 'yes' in finally_answer.lower():
                    yes_count += 1
                elif 'no' in finally_answer.lower():
                    no_count += 1

            print("\033[1;32m------------------------------------ GET_END ----------------------------------------\033[0m")

            # 根据统计结果返回yes或no
            if yes_count >= 2:
                print("External knowledge is required (yes).")
                return 'yes'
            elif no_count >= 2:
                print("External knowledge is not required (no).")
                return 'no'
            else:
                print("Could not determine if external knowledge is required.")
                return "Unknown response"

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
