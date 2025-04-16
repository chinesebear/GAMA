import transformers
import torch

# 设置模型ID和本地保存路径
model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
save_directory = "./my_llama_model"

# 下载并保存模型到指定目录
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    cache_dir=save_directory
)

tokenizer = transformers.AutoTokenizer.from_pretrained(
    model_id,
    cache_dir=save_directory
)

# 创建推理pipeline
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
)

# 测试模型输出
messages = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

outputs = pipeline(messages, max_new_tokens=256)

# 打印结果
print(outputs[0]["generated_text"])
