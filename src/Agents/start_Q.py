import asyncio
from src.Agents.roles.logic_expert import PlanerLogic
from src.Agents.roles.problem_classification_major import ProblemClassification
from src.Agents.find_answer import FinalAnswerExtractor
from src.Agents.planer import Planner
import re
class QuestionProcessor:
    def __init__(self):
        self.problem_classifier = ProblemClassification()
        self.phrase ="Final answer:"

    def extract_text(self, text):
        # 使用正则表达式从特定短语到 // 之间匹配内容
        pattern = re.escape(self.phrase) + r"(.+?)//"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()  # 返回匹配的内容，并去除两端的空白字符
        return "no answer"  # 如果没有找到匹配，返回空字符串



    async def process_question(self, question,id_=None):
        result = await self.problem_classifier.repair(question)
        if result == 'yes':
            # 如果需要外部知识，则可以在这里执行相关操作
             planner = Planner(question)
             fusion_answers,answers,final_answer = await planner.run()
             return fusion_answers,answers,final_answer
        elif result == 'no':

            #logic = PlanerLogic()
            #省略步骤

            #file_path = '/mnt/c/workspace/code/xagent_zhao/data/logic_grid_puzzle/logic_grid_puzzle_200.jsonl__method-spp_engine-devgpt4-32k_temp-0.0_topp-1.0_start0-end200__without_sys_mes.jsonl'
            #extractor = FinalAnswerExtractor(file_path)
            #answer =extractor.get_answer_by_index(id_) # Get the first answer
            #print("☆☆☆☆☆☆First Answer:",answer)
            logic = PlanerLogic()
            answer = await logic.logic(question)
            answer_is,contradiction_info = await logic.verify(question,answer)
            if answer_is:
                return answer,answer,answer
            else:
                for i in range(3):
                    memory = str(contradiction_info)
                    answer = await logic.logic_again(question,answer,memory)
                    answer = self.extract_text(answer)
                    print("☆☆☆☆☆new answer:",answer)
                    answer_is,contradiction_info=await logic.verify(question,answer)
                    if answer_is:
                        break
            return answer,answer,answer



        else:
            print("Unable to determine if external knowledge is required")
            answer = None  # 确保 answer 被定义，无论结果如何
            return answer

