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

import re


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
        start_line = 0
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
                print('question:', data.get('question'))
                email = data.get('question')
                print('answers:', data.get('answers'))
                print('privacy_data:', data.get('privacy_data'))
                print('-----------------------------------')
                task = 'Write a reply to the letter by answering the questions in the form of a story, below:\n{email}'
                task_all = task.format(email=email)
                print(data['answers'])
                """NER_question, replacement_dict, masked_question = await privacy_part(task_all)
                # 实例化 LLMpp 类
                llm_instance = LLMpp()
                LLM_masked_question = await llm_instance.llm_ppagent(task_all)"""

                """(
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

                answer_plan_matches, answer_repair_matches, answer_plan_matches_sub = await process_answers(task_all,
                                                                                                          line_number,
                                                                                                            data)
                #ner_answer = await runner.execute(NER_question)
                #answer_ner_matches = count_nested_answers_in_text(ner_answer, data['answers'])
                #llm_answer =await runner.execute(LLM_masked_question)
                #answer_llm_matches = count_nested_answers_in_text(llm_answer, data['answers'])
                base_answer = await runner.execute(task_all)
                answer_base_matches = count_nested_answers_in_text(base_answer, data['answers'])
                sum1 = answer_plan_matches + sum1
                sum2 = answer_repair_matches + sum2
                sum3 = answer_plan_matches_sub + sum3
                #sum4 = answer_ner_matches +sum4
                #sum5 = answer_llm_matches +sum5
                sum6 = answer_base_matches+sum6
                print('my: The number of correct answers to the verification sub_questions:', sum3)
                print('my:The number of correct answers after the repair:', sum2)
                print('my:The number of correct answers:', sum1)
                #print("ner:",sum4)
                #print("llm:",sum5)
                print("base:",sum6)

            """calculate_and_print_metrics(
                scores_ner, scores_2_ner, missing_count_ner_sum, non_privacy_count_ner_sum,
                scores_llm, scores_2_llm, missing_count_llm_sum, non_privacy_count_llm_sum,
                scores_mask, scores_2_mask, missing_count_mask_sum, non_privacy_count_mask_sum,
                ner_bleu_scores, ner_semantic_similarities,
                llm_bleu_scores, llm_semantic_similarities,
                mask_bleu_scores, mask_semantic_similarities
            )"""


    except Exception as e:
        print(f"An error occurred: {e}")

# 设置开始处理的样本序号


# 调用异步函数
asyncio.run(read_json_file('/home/zhaorh/code/ppagent/data/wki/HotpotQA/emails.json'))

