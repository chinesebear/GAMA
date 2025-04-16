# utils.py 或适当的模块中

from src.Agents.API_info import ChatActionRunner
import logging
from src.Agents.API_info import ChatActionRunner
from src.Agents.start_Q import QuestionProcessor
from src.Agents.memory import config_w2v


# 初始化配置
config_w2v.initialize_calculator()
logger = logging.getLogger('chat')

class ChatService:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.processor = QuestionProcessor()

    async def get_response(self, user_question: str) -> str:
        try:
            response = await self.runner.execute(user_question)
            return response
        except RuntimeError as e:
            logger.error(f"获取AI回应时出错: {e}")
            return "抱歉，我无法处理您的请求。"


    async def handle_question(self, question: str, line_number=None):
        """
        Process the given question and return the results.

        :param question: The question to process.
        :param line_number: Optional, line number for processing context.
        :return: A dictionary containing plan_answer, answers, and final_answer.
        """
        try:
            # 调用 QuestionProcessor 处理问题
            plan_answer, answers, final_answer = await self.processor.process_question(question, line_number)

            # 构建结果字典
            result = plan_answer


            return result
        except Exception as e:
            # 捕获异常并打印错误信息
            print(f"An error occurred while processing the question: {e}")
            return None


