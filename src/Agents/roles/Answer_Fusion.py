from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio

class AnswerFusion:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.expert_fusion = Columbus.Answer_Fusion_Prompt

    async def fusion(self, task,results):
        try:
            content = ""
            number = 1
            for result in results:
                content = content + str(number) + ':' + result
                number += 1
            all_answer= self.expert_fusion.format(task=task,content=content)
            print("------------------------------------Answer_Fusion---------------------------------------------")

            # Execute the query asynchronously
            final_answer = await self.runner.execute(all_answer)
            print("------------------------------------Fusion_end------------------------------------------------")

            # Extract and return the relevant message from the response

            return final_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None