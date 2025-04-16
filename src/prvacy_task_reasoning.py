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
from src.Agents.memory import config_w2v
from src.Agents.API_info import ChatActionRunner
config_w2v.initialize_calculator()

import re

def evaluate_answer(text, standard_answer):
    # 如果 text 是列表，将其转换为一个字符串
    print(text)
    if isinstance(text, list):
        text = ' '.join(map(str, text))  # 将列表元素连接为一个字符串

    # 确保 text 和 standard_answer 都是字符串类型，并忽略大小写
    text_str = str(text).strip().lower()
    standard_answer_str = str(standard_answer).strip().lower()

    # 使用正则表达式来匹配标准答案作为完整单词出现
    if re.search(rf'\b{re.escape(standard_answer_str)}\b', text_str):
        return 1
    else:
        return 0


async def process_answers(task_all, line_number, data):
    processor = QuestionProcessor()
    plan_answer, answers, final_answer = await processor.process_question(task_all, line_number)

    print('Fusion final answer:', plan_answer)
    print('SUB ANSWER:', answers)
    print('Repair fusion final answer:', final_answer)

    sub_a = " ".join(answers)
    print('+++++sub_question++++++')
    answer_plan_matches_sub = count_nested_answers_in_text(sub_a, data['answers'])
    print(f"SUB Number of plan answers found in story: {answer_plan_matches_sub}")

    print('+++++plan_question++++++')
    answer_plan_matches = count_nested_answers_in_text(plan_answer, data['answers'])
    print(f"Number of fusion answers found in story: {answer_plan_matches}")

    if "perfect" in final_answer.lower():  # Check for 'perfect' case-insensitively
        print('+++++plan_repair_question++++++')
        answer_repair_matches = answer_plan_matches
    else:
        print('+++++plan_repair_question++++++')
        answer_repair_matches = count_nested_answers_in_text(final_answer, data['answers'])
        print(f"Number of fusion answers found in story: {answer_repair_matches}")

    return answer_plan_matches, answer_repair_matches, answer_plan_matches_sub


async def read_json_file(file_path):
    llm_bleu_scores = []
    llm_semantic_similarities = []
    ner_bleu_scores = []
    ner_semantic_similarities = []
    mask_bleu_scores = []
    mask_semantic_similarities = []
    scores_ner = dict(name=0, location=0, organization=0, email_id=0)
    scores_2_ner = {'name': 0, 'location': 0, 'organization': 0, 'email_id': 0}
    scores_llm = {'name': 0, 'location': 0, 'organization': 0, 'email_id': 0}
    scores_2_llm = {'name': 0, 'location': 0, 'organization': 0, 'email_id': 0}
    scores_mask  = {'name': 0, 'location': 0, 'organization': 0, 'email_id': 0}
    scores_2_mask = {'name': 0, 'location': 0, 'organization': 0, 'email_id': 0}
    missing_count_ner_sum = 0
    non_privacy_count_ner_sum = 0
    missing_count_llm_sum = 0
    non_privacy_count_llm_sum = 0
    missing_count_mask_sum = 0
    non_privacy_count_mask_sum = 0

    runner = ChatActionRunner()
    """
    读取 JSON 文件，对每个样本执行处理，并在用户按 Enter 确认后继续。
    """
    try:
        start_line = 1
        sum1 =0
        sum2 =0
        sum3 =0
        sum4 =0
        sum5 =0
        sum6 =0

        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
            data_list = json.loads(content)
            for line_number, data in enumerate(data_list, start=1):
                if line_number < start_line:
                    continue
                print('id:', data.get('id'))
                print('question:', data.get('passage'))
                email = data.get('passage')
                print('answers:', data.get('answer'))
                print('privacy_data:', data.get('privacy_data'))
                print('-----------------------------------')
                task = '''Please respond to the following letter by choosing either “True” or “False”:
                        - If your answer is “True,” ensure the reply contains no mention of “False” anywhere.
                        - If your answer is “False,” ensure the reply contains no mention of “True” anywhere. below:\n{email}'''
                task_all = task.format(email=email)
                print(data['answer'])
                NER_question, replacement_dict, masked_question = await privacy_part(task_all)
                """# 实例化 LLMpp 类
                llm_instance = LLMpp()
                LLM_masked_question = await llm_instance.llm_ppagent(task_all)

                (
                    scores_ner, scores_2_ner,
                    scores_llm, scores_2_llm,
                    scores_mask, scores_2_mask,
                    ner_bleu_scores, ner_semantic_similarities,
                    llm_bleu_scores, llm_semantic_similarities,
                    mask_bleu_scores, mask_semantic_similarities,
                    missing_count_ner_sum, non_privacy_count_ner_sum,
                    missing_count_llm_sum, non_privacy_count_llm_sum,
                    missing_count_mask_sum, non_privacy_count_mask_sum
                ) = process_privacy_scores_and_metrics(
                    scores_ner, scores_2_ner,
                    scores_llm, scores_2_llm,
                    scores_mask, scores_2_mask,
                    NER_question, LLM_masked_question, masked_question,
                    data, task_all,
                    ner_bleu_scores, ner_semantic_similarities,
                    llm_bleu_scores, llm_semantic_similarities,
                    mask_bleu_scores, mask_semantic_similarities,
                    missing_count_ner_sum, non_privacy_count_ner_sum,
                    missing_count_llm_sum, non_privacy_count_llm_sum,
                    missing_count_mask_sum, non_privacy_count_mask_sum
                )"""
                processor = QuestionProcessor()
                plan_answer, answers, final_answer = await processor.process_question(masked_question, line_number)
                #ner_answer = await runner.execute(NER_question)
                #llm_answer =await runner.execute(LLM_masked_question)
                base_answer = await runner.execute(task_all)

                if "perfect" in final_answer.lower():
                    final_answer = plan_answer
                standard_answer = data.get('answer')
                print("标准答案",standard_answer)
                # 初始化各个 sum 变量
                sum11 = evaluate_answer(plan_answer, standard_answer)
                sum22 = evaluate_answer(final_answer, standard_answer)
                sum33 = evaluate_answer(answers, standard_answer)
                #sum44 = evaluate_answer(ner_answer, standard_answer)
                #sum55 = evaluate_answer(llm_answer, standard_answer)
                sum66 = evaluate_answer(base_answer, standard_answer)
                sum1 = sum11 + sum1
                sum2 = sum22 + sum2
                sum3 = sum33 + sum3
                #sum4 = sum44 + sum4
                #sum5 = sum55 + sum5
                sum6 = sum66 + sum6
                print('my:The number of correct answers after the repair:',final_answer)
                print('my:The number of correct answers:', plan_answer)
                print('my: The number of correct answers to the verification sub_questions:', sum3)
                print('my:The number of correct answers after the repair:', sum2)
                print('my:The number of correct answers:', sum1)
                #print("ner:",sum4)
                #print("llm:",sum5)
                print("base:",sum6)
            calculate_and_print_metrics(
                scores_ner, scores_2_ner, missing_count_ner_sum, non_privacy_count_ner_sum,
                scores_llm, scores_2_llm, missing_count_llm_sum, non_privacy_count_llm_sum,
                scores_mask, scores_2_mask, missing_count_mask_sum, non_privacy_count_mask_sum,
                ner_bleu_scores, ner_semantic_similarities,
                llm_bleu_scores, llm_semantic_similarities,
                mask_bleu_scores, mask_semantic_similarities
            )

    except Exception as e:
        print(f"An error occurred: {e}")

# 设置开始处理的样本序号


# 调用异步函数
asyncio.run(read_json_file('/home/zhaorh/code/ppagent/data/pp_data/reasoning_pp.json'))


