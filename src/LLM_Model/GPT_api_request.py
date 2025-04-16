from openai import OpenAI
import datetime
class ChatClient:
    def __init__(self, api_key, base_url='https://api.openai-proxy.org/v1'):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def fetch_chat_response(self, user_input, model, temperature=0.0):
        # 这里示例中的模型调用现在指定为assistant回应
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Current Time: {current_time}")
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "assistant", "content": user_input},
            ],
            model=model,
            temperature=temperature,
            top_p = 1.0
        )
        print(f"API Endpoint: {self.client.base_url}")
        print(f"Model Used: {model}")
        print(f"MODEL Response: ",chat_completion)
        return chat_completion


