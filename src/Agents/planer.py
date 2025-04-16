import asyncio
from src.Agents.roles.collector import QuestionCollector
from src.text_analysis.TF_IDF import TextDomainAnalyzer
from src.Agents.roles.expert_doing import ExpertCooperation
from src.Agents.roles.select_experter import ExpertSelector, IndustryExtractor
from src.Agents.roles.Answer_Fusion import AnswerFusion
from src.Agents.roles.Repairman import RepairPerson
from src.Agents.memory.Disassembly_Problem import DisassemblyProblem
from src.Agents.roles.sub_q_check import SubCheckMan
import re
from src.Agents.expert import ExpertPick
from src.Agents.demo2 import Answer
# 异步主函数
class Planner:
    def __init__(self, question):
        self.fields = None
        self.question = question

    def create_expert_sentences(self):
        # 用来存储生成的句子
        sentences = []

        # 遍历 fields 列表并生成句子
        for field, level in self.fields:
            sentence = f"You are an expert in {field} with an {level} level of expertise."
            sentences.append(sentence)

        return sentences

    async def run(self):
        dis_question =DisassemblyProblem()
        questions_sub = await dis_question.disassembly(questions=self.question)
        print(questions_sub)
        results = []
        a_questions = re.findall(r'//\s*(.*?)\s*//', questions_sub)
        print(a_questions)
        for i, a_question in enumerate(a_questions, 1):
            #领域专家
            a = Answer()
            processor = ExpertPick()
            expert_prompt,self.fields = await processor.process(a_question)
            sentences = self.create_expert_sentences()
            field_results = []
            for sentence in sentences:
                print(sentence)
                field_result = await a.answer_sub(a_question,sentence,"")
                print(field_result)
                field_results.append(field_result)
            print(field_results)
            final_sentence = " ".join(field_results)
            result = await a.answer_sub(a_question,expert_prompt,final_sentence)
            print(result)
            if result is None:
                expert_prompt ='you are a expert,'
                result = await a.answer_sub(a_question, expert_prompt,final_sentence)
            b = result
            print('sub question result:',result)
            max_iterations = 4  # 设置最大循环次数
            iterations = 0  # 初始化计数器
            check_result_man = SubCheckMan()
            contradictions = True
            while contradictions and iterations < max_iterations:
                # Check if the result is correct using the check method
                check_result = await check_result_man.check(a_question, result)

                if isinstance(check_result, tuple) and len(check_result) == 2:
                    # If the check returns a tuple, evaluate the result
                    contradictions = not check_result[0]  # Set contradictions based on check_result[0]
                    result = check_result[1]  # Update the result
                elif isinstance(check_result, bool):
                    # If the check returns a boolean, set contradictions based on its value
                    contradictions = not check_result  # Set contradictions based on check_result
                else:
                    # Handle unexpected result format
                    contradictions = True

                # Update iterations and print current state
                iterations += 1
            if result =='No answer found':
                result = b
            results.append(result)
        answer_fusion = AnswerFusion()
        fusion_answer = await answer_fusion.fusion(self.question,results)
        finally_answer = RepairPerson()
        final_answer = await finally_answer.repair(self.question, results,fusion_answer)

        return fusion_answer,results,final_answer




