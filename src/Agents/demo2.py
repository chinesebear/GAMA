from src.Agents.roles import Columbus
from src.Agents.API_info import ChatActionRunner
import asyncio



class Answer:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.question_format_0 = '''Answer this question：{Question}，
        The answer should be as comprehensive as possible and should not exceed 20 words.
        Please read my question carefully, grasp every word accurately, and answer after sufficient reasoning.
        If it is a binary question, answer true or false.
        If it is a question about the timeline, please search your knowledge base based on the question and think carefully before answering.
        '''

        self.question_format_1 = '''Answer this question：{Question}，
                You can refer to the answers to these:{some_answers}
                The answer should be as comprehensive as possible and should not exceed 20 words.
                Please read my question carefully, grasp every word accurately, and answer after sufficient reasoning.
                If it is a binary question, answer true or false.
                If it is a question about the timeline, please search your knowledge base based on the question and think carefully before answering.
                '''

    async def answer_sub(self, question,prompt,some_answers):
        try:

            if not some_answers:  # 如果 some_answers 为空
                # 执行 A 操作（按你原来的逻辑构建 all_content）
                all_content = self.question_format_0.format(Question=question)
                all_content = prompt  + all_content
                print('prompt for sub_field_question', all_content)
                print("------------------------------------Sub-questions----------------------------------------")
                # 并行执行多个异步操作
                finally_answer = await self.runner.execute(all_content)


            else:  # 如果 some_answers 不为空，执行 B 操作
                # 假设 B 操作是修改 all_content 或其他操作
                all_content = self.question_format_1.format(Question=question,some_answers =some_answers)
                all_content = prompt + all_content
                print('sub question', all_content)
                print("------------------------------------Sub-questions----------------------------------------")

                # 并行执行多个异步操作
                finally_answer = await self.runner.execute(all_content)

            print("------------------------------------end----------------------------------------")
            return finally_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


"""import asyncio

# Assuming the Answer class is imported or defined in your script

# Create an instance of the Answer class
answer_instance = Answer()

# Define the question and prompt you want to pass
question = "How many runs did Donald Bradman score in his last ever test match innings?"
prompt = "you are a expert. "

# Use asyncio to run the answer_sub method, since it's an async function
async def get_answer():
    result = await answer_instance.answer_sub(question, prompt)
    print(f"Answer: {result}")

# Run the async function
asyncio.run(get_answer())"""
