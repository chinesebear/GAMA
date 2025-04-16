from transformers import pipeline, set_seed
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

def finance_generate_text(text, model_path):
    # 检查CUDA是否可用
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    model_path = "C:/Users/zrh/.cache/huggingface/hub/models--lxyuan--distilgpt2-finetuned-finance/snapshots/e185be9dba22a0c041b26293483b55e39461119b"  # 替换为你的模型路径
    # 加载模型
    generator = pipeline("text-generation", model=model_path, device=device.index if device.type == "cuda" else -1)

    # 生成文本
    generated_texts = generator(
        text,
        pad_token_id=generator.tokenizer.eos_token_id,
        max_new_tokens=200,
        num_return_sequences=2
    )

    return generated_texts

def gpt2_generate_text(prompt):
    # 配置GPU设备
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    # 初始化模型和分词器
    tokenizer = GPT2Tokenizer.from_pretrained('C:/Users/zrh/.cache/huggingface/hub/models--distilgpt2\snapshots/38cc92ec43315abd5136313225e95acc5986876c')
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model = GPT2LMHeadModel.from_pretrained('C:/Users/zrh/.cache/huggingface/hub/models--FredZhang7--distilgpt2-stable-diffusion-v2/snapshots/f839bc9217d4bc3694e4c5285934b5e671012f85').to(device)

    temperature = 0.9
    top_k = 8
    max_length = 80
    repetition_penalty = 1.2
    num_return_sequences = 5

    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(device)

    # 在GPU上运行生成
    output = model.generate(
        input_ids,
        do_sample=True,
        temperature=temperature,
        top_k=top_k,
        max_length=max_length,
        num_return_sequences=num_return_sequences,
        repetition_penalty=repetition_penalty,
        penalty_alpha=0.6,
        no_repeat_ngram_size=1,
        early_stopping=True
    )

    results = []
    for i in range(len(output)):
        results.append(tokenizer.decode(output[i], skip_special_tokens=True))

    return results



def legal_generate_text(text):
    import torch
    if torch.cuda.is_available():
        device = 0
    else:
        device = -1

    set_seed(42)

    # 修改这里来从本地加载模型
    model_path = 'C:/Users/zrh/.cache/huggingface/hub/models--umarbutler--open-australian-legal-distilgpt2/snapshots/06071d63a090272147154ebaf04f61df471cdbcf'  # 你的本地模型路径
    generator = pipeline('text-generation', model=model_path, device=device)

    generated_text = generator(text, max_length=50, num_return_sequences=5)
    generated_text = [result['generated_text'] for result in generated_text]

    return generated_text


def medical_generation(text):
    import torch
    if torch.cuda.is_available():
        device = 0
    else:
        device = -1

    set_seed(42)

    # 修改这里来从本地加载模型
    model_path = 'C:/Users/zrh/.cache/huggingface/hub/distilgpt2-finetuned-medical'  # 你的本地模型路径
    generator = pipeline('text-generation', model=model_path, device=device)

    generated_text = generator(text, max_length=50, num_return_sequences=5)
    generated_text = [result['generated_text'] for result in generated_text]

    return generated_text
'''
 

text = "Your input text here"
generated_texts = generate_text(text)
print(generated_texts)
'''
