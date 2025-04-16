import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class TextGenerator:
    def __init__(self, model_path):
        # 指定使用显卡1
        self.device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")

        # 初始化 tokenizer 和 model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token  # 设置 pad_token

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map=None  # 不自动映射，手动指定设备
        ).to(self.device)  # 将模型加载到显卡1

    def generate_text(self, messages, document):
        # 格式化输入文本
        formatted_input = self._get_formatted_input(messages, document)
        print(f"Formatted Input:\n{formatted_input}")

        # Tokenize 输入文本并移动到模型设备
        tokenized_prompt = self.tokenizer(
            self.tokenizer.bos_token + formatted_input,
            return_tensors="pt",
            truncation=True,  # 确保输入长度不会超出模型的限制
            max_length=1024  # 控制最大输入长度
        ).to(self.device)  # 将输入数据移动到显卡1

        # 设置结束符
        eos_token_id = self.tokenizer.eos_token_id

        # 使用模型生成文本
        outputs = self.model.generate(
            input_ids=tokenized_prompt.input_ids,
            attention_mask=tokenized_prompt.attention_mask,
            max_new_tokens=256,
            eos_token_id=eos_token_id,
            do_sample=True,  # 控制生成更自然的回答
            temperature=0.6,  # 调节生成的多样性
            top_p=1.0,  # 使用 nucleus sampling
            pad_token_id=self.tokenizer.pad_token_id
        )

        # 解码生成的文本
        response = outputs[0][tokenized_prompt.input_ids.shape[-1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)

    def _get_formatted_input(self, messages, context):
        # 构建格式化输入
        system_prompt = (
            "System: This is a chat between a user and an artificial intelligence assistant. "
            "The assistant gives helpful, detailed, and polite answers to the user's questions based on the context."
        )
        conversation = '\n\n'.join(
            ["User: " + item["content"] for item in messages if item['role'] == "user"]
        ) + "\n\nAssistant:"
        formatted_input = f"{system_prompt}\n\n{context}\n\n{conversation}"
        return formatted_input
