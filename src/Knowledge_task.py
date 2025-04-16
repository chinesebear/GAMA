import json
import asyncio
from src.Agents.start_Q import QuestionProcessor
from src.Agents.memory import config_w2v
config_w2v.initialize_calculator()
import re


def count_nested_answers_in_text(text, nested_answers):
    """
    计算文本中包含给定答案列表中的答案个数。
    每个子列表视为一个单独的得分单位，如果文本包含子列表中的任何一个答案，则得分加一。
    使用正则表达式确保匹配完整单词边界。
    特别处理类似“12th”匹配“12”的情况，以及处理部分匹配（如“answer”匹配“ans”）。

    参数:
    - text (str): 需要检查的文本。
    - nested_answers (list of list of str): 嵌套答案列表。

    返回:
    - int: 总得分。
    """
    lower_text = text.lower()
    total_score = 0
    a = 1

    for answers in nested_answers:
        found = False

        for answer_set in answers:
            words = answer_set.lower().split()
            # Check if all words in the answer are present in the text
            if all(
                re.search(r'\b' + re.escape(word) + r'[a-z]*s?\b', lower_text) for word in words
            ):
                # Special handling for numeric answers with suffixes
                if any(word.isdigit() for word in words):
                    if all(
                        re.search(r'\b' + re.escape(word) + r'(?:st|nd|rd|th)?\b', lower_text) for word in words
                    ):
                        print(f'The {a} correct answer is identified. The correct answer is {answer_set}')
                        found = True
                        break
                else:
                    print(f'The {a} correct answer is identified. The correct answer is {answer_set}')
                    found = True
                    break

        if found:
            total_score += 1
        else:
            print(f'The correct answer was not identified for the {a} one, and the solution does not have the following answer: {answers}')

        a += 1

    return total_score


async def read_jsonl_file(file_path):
    sum1 = 0
    sum2 = 0
    start_line = 1
    sum3 = 0
    """
    逐行读取 JSONL 文件，对每个样本执行答案检查，并在用户按 Enter 确认后继续。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if line_number < start_line:
                    continue  # Skip lines until the specified start line

                data = json.loads(line)
                processor = QuestionProcessor()
                if 'questions' in data and 'answers' in data:
                    print("NO：", line_number)
                    print("Topic:", data['topic'])
                    n = len(data['question_ids'])
                    # 假设standard.demo()返回问题的标准答案列表
                    task = 'Write a short and coherent story about {topic} that incorporates the answers to the following {n} questions: {questions}'
                    questions_str = " ".join(data['questions'])
                    task_all =task.format(topic =data['topic'],n=n,questions =questions_str)
                    print(task_all)
                    #answer_standards = await standard.demo(task_all)
                    #print('标准答案：',answer_standards)
                    #answer_standards_matches = count_nested_answers_in_text(answer_standards, data['answers'])
                    #print(f"Number of standards answers found in story: {answer_standards_matches}")
                    #sum2 = answer_standards_matches + sum2
                    #print('标准版答对的个数', sum2)
                    plan_answer,answers,final_answer = await processor.process_question(task_all, line_number)
                    print('fusion finally answer:',plan_answer)
                    print('SUB ANSWER',answers)
                    print('repair fusion finally answer:',final_answer)
                    sub_a=" ".join(answers)
                    print('+++++sub_question++++++')
                    answer_plan_matches_sub = count_nested_answers_in_text(sub_a, data['answers'])
                    print(f"SUB Number of plan answers found in story: {answer_plan_matches_sub}")
                    print('+++++plan_question++++++')
                    answer_plan_matches = count_nested_answers_in_text(plan_answer, data['answers'])
                    print(f"Number of fusion answers found in story: {answer_plan_matches}")

                    if "perfect" in  final_answer.lower():  # 不区分大小写地检查是否包含 'perfect'
                        # 执行操作 A
                        print('+++++plan_repair_question++++++')
                        answer_repair_matches=answer_plan_matches
                    else:
                        print('+++++plan_repair_question++++++')
                        answer_repair_matches = count_nested_answers_in_text(final_answer, data['answers'])
                        print(f"Number of fusion answers found in story: {answer_repair_matches}")
                    sum1 = answer_plan_matches + sum1
                    sum2 =answer_repair_matches +sum2
                    sum3 = answer_plan_matches_sub +sum3
                    print('The number of correct answers to the verification sub_questions:',sum3)
                    print('The number of correct answers after the repair:',sum2)
                    print('The number of correct answers',sum1)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    file_path = '../data/SSP/trivia_creative_writing_100_n_5.jsonl'
    await read_jsonl_file(file_path)


# 运行主函数
asyncio.run(main())
