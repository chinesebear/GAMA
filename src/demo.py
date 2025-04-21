
import asyncio
from src.Agents.start_Q import QuestionProcessor
from src.Agents.memory import config_w2v
config_w2v.initialize_calculator()

async def main():
    question = ""
    processor = QuestionProcessor()
    line_number = None
    plan_answer, answers, final_answer = await processor.process_question(question, line_number)
# 运行异步任务
asyncio.run(main())