from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio
import json
import asyncio
import aiofiles
from src.Agents.start_Q import QuestionProcessor
from src.Agents.memory import config_w2v
from src.Agents.privacy_part import privacy_part
config_w2v.initialize_calculator()
from src.LLM_pp_agent import LLMpp
import re
from src.Evaluation import *


async def main():
    question = "aswdadas"
    processor = QuestionProcessor()
    line_number = None
    plan_answer, answers, final_answer = await processor.process_question(question, line_number)




# 运行异步任务
asyncio.run(main())