import asyncio
from src.Agents.actions.action import Action
from src.LLM_Model.GPT_api_request import ChatClient

class ChatActionRunner:
    def __init__(self, model="gpt-4o"):
        self._api_key = 'sk-nTaeIVSY4P3w9dnLXQa5ar1xIKhE04dL1D6pXmG4JUabvnnG'  # API key is now a fixed, private attribute
        self._model = model
        self._chat_client = ChatClient(self._api_key)
        self._action = Action(self._chat_client)

    async def _run_action(self, content):
        try:
            response = await self._action.run(content, self._model)
            # Extract the final answer here
            answer = response['choices'][0]['message']['content']
            return answer
        except Exception as e:
            # Log the exception, raise an error, or handle it as needed
            raise RuntimeError(f"An error occurred during the API request: {str(e)}")

    async def execute(self, content):
        # Directly await the private method without using asyncio.run
        try:
            return await self._run_action(content)
        except RuntimeError as e:
            # Handle the error or rethrow it after logging
            print(e)
            return {"error": str(e)}


'''import aiohttp
import asyncio

class ChatActionRunner:
    def __init__(self, model="llama3.1:70b"):
        self._model = model
        self._url = 'http://172.18.144.13:11434/api/chat'

    async def _run_action(self, content):
        try:
            data = {
                "model": self._model,
                "messages": [{ "role": "user", "content": content }],
                "stream": False
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(self._url, json=data) as response:
                    response.raise_for_status()  # Raise exception for HTTP errors
                    result = await response.json()
                    # Return only the content of the assistant's message
                    return result.get('message', {}).get('content', 'No content in response')
        except Exception as e:
            # Log the exception, raise an error, or handle it as needed
            raise RuntimeError(f"An error occurred during the API request: {str(e)}")

    async def execute(self, content):
        # Directly await the private method without using asyncio.run
        try:
            return await self._run_action(content)
        except RuntimeError as e:
            # Handle the error or rethrow it after logging
            print(e)
            return {"error": str(e)}
'''


