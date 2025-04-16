import asyncio
from src.Agents.API_info import ChatActionRunner


class LLMpp:
    def __init__(self):
        self.runner = ChatActionRunner()
        self.question_format = '''You are an assistant responsible for ensuring compliance with the GDPR (General Data Protection Regulation).  
Your task is to carefully identify and redact all personal or sensitive data from the following content while preserving the context and instructions.

Here is the task content, which includes specific questions and instructions:

//{question}//

The categories of data you need to protect include, but are not limited to:
1. **Personal identifiers** (e.g., full names, initials, usernames, or pseudonyms).  
2. **Location data** (e.g., any city, address, or geographical location).  
3. **Contact information** (e.g., phone numbers, email addresses, or mailing addresses).  
4. **Organizational affiliations** (e.g., memberships, employment details, or associations).  

Please redact the necessary personal or sensitive information using the following format:
1. **Personal identifiers** (e.g., full names, initials, usernames, or pseudonyms).  =
   - Format: `<name-1>`, `<name-2>`, etc.
2. **Location data** (e.g., any city, address, or geographical location).  
   - Format: `<location-1>`, `<location-2>`, etc.
3. **Contact information** (e.g., phone numbers, email addresses, or mailing addresses).  
   - Format: `<contact-1>`, `<contact-2>`, etc.
4. **Organizational affiliations** (e.g., memberships, employment details, or associations).  
   - Format: `<organization-1>`, `<organization-2>`, etc.

Return the processed content with sensitive data replaced as per the format above, ensuring the original structure and instructions remain intact.
....
        '''




    async def llm_ppagent(self, question: str):
        try:
            # 确保 question 是字符串
            if not isinstance(question, str):
                raise ValueError("Question must be a string.")

            all_content = self.question_format.format(question=question)

            print('Sub-question generated:', all_content)
            print("----------------------------------------------------------------------------")

            # 执行异步操作
            finally_answer = await self.runner.execute(all_content)
            print("------------------------------------End----------------------------------------")
            return finally_answer
        except Exception as e:
            print(f"An error occurred: {e.__class__.__name__} - {str(e)}")
            return None

