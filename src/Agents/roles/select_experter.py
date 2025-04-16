import re

from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio

class ExpertSelector:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.expert_handler = Columbus.analyzy

    async def elector_expert(self, collect_information):
        try:
            experts = self.expert_handler.format(collect_information=collect_information)

            print("------------------------------------collect_information----------------------------------------")

            # Execute the query asynchronously
            related_message = await self.runner.execute(experts)
            print("------------------------------------collect_end----------------------------------------")

            # Extract and return the relevant message from the response

            return related_message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


class IndustryExtractor:
    def __init__(self, text):
        self.text = text

    def extract(self):
        # 使用正则表达式来查找标题和相关度分数
        pattern = r'\*\*(.*?)\*\*\s*Relevance\s*Score:\s*(\w+(?:\s\w+)*)'
        # 查找所有符合条件的匹配
        results = re.findall(pattern, self.text, re.IGNORECASE | re.DOTALL)

        # 移除标题中不需要的单词'Industry'
        cleaned_results = [(title.replace('Industry', '').strip(), score) for title, score in results]
        return cleaned_results
