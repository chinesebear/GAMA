from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio
import re


def extract_and_check(text):
    try:
        # 查找第一个 // 的位置
        start = text.find("//")
        if start != -1:
            # 查找第二个 // 的位置
            end = text.find("//", start + 2)
            if end != -1:
                # 提取第一个 // 之间的内容
                content = text[start + 2:end].strip()

                # 检查内容是否包含 "correct"
                if "correct" in content:
                    return True
                elif "wrong" in content:
                    # 检查后续内容是否包含 "answer:"
                    answer_start = text.find("answer：", end)
                    if answer_start != -1:
                        # 提取 "answer:" 后面的内容
                        answer_content = text[answer_start + len("answer:"):].strip()
                        return False, answer_content
                    else:
                        return False, "No answer found"
        return "No content found"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class SubCheckMan:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.repairman = Columbus.sub_repairman

    async def check(self, question,answer):
        try:
            all_content = self.repairman.format(question=question,answer=answer)
            print("\033[1;32m------------------------------------ Sub_question-Check ----------------------------------------\033[0m")

            # 并行执行多个异步操作
            output =   await self.runner.execute(all_content)

            print(output)
            result2 = extract_and_check(output)
            print("\033[1;32m------------------------------------ Sub_question-Check-End ----------------------------------------\033[0m")
            return result2
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

