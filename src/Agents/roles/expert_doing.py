from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio


class ExpertCooperation:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.expert_handler = Columbus.experts

    async def elector_expert(self, results,question):
        try:
            tasks = []
            print("\033[1;32m------------------------------------ Expert analysis ----------------------------------------\033[0m")
            for title, score in results:
                print(f"Title: {title}, Relevance Score: {score}")
                experts = self.expert_handler.format(field=title, score=score,question=question)
                task = self.runner.execute(experts)
                tasks.append(task)

            # Await all scheduled tasks
            responses = await asyncio.gather(*tasks)
            print("\033[1;32m------------------------------------ Expert analysis_end ----------------------------------------\033[0m")
            # Extract and return the relevant messages from all responses
            related_messages = responses

            return related_messages
        except Exception as e:
            print(f"An error occurred: {e}")
            return None