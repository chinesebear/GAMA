from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class TextGenerator:
    def __init__(self, model_path):
        # 初始化时加载模型和tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map="auto")

    def generate_text(self, messages, document):
        # 格式化输入文本
        formatted_input = self._get_formatted_input(messages, document)
        # Tokenize输入文本
        tokenized_prompt = self.tokenizer(self.tokenizer.bos_token + formatted_input, return_tensors="pt").to(self.model.device)
        # 设置结束符
        terminators = [self.tokenizer.eos_token_id]
        # 使用模型生成文本
        outputs = self.model.generate(
            input_ids=tokenized_prompt.input_ids,
            attention_mask=tokenized_prompt.attention_mask,
            max_new_tokens=128,
            eos_token_id=terminators
        )
        # 解码生成的文本
        response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)

    def _get_formatted_input(self, messages, context):
        system = "System: This is a chat between a user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions based on the context."
        conversation = '\n\n'.join(
            ["User: " + item["content"] for item in messages if item['role'] == "user"]) + "\n\nAssistant:"
        formatted_input = system + "\n\n" + context + "\n\n" + conversation
        return formatted_input

# 使用
model_path = "/home/zhaorh/code/ppagent/model/Llama-7B"
generator = TextGenerator(model_path)
document = """Were Thinking Fellers Union Local 282 and the Smiths, who had a lead singer of Morrissey, both active in 1986?"""
messages = [{"role": "user", "content": "Extract the names of people from the document."}]

response = generator.generate_text(messages, document)
print(response)
