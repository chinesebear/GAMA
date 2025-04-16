import re
import asyncio
from src.Agents.memory.NER import get_encryptor
from src.Agents.memory.llama_8B import TextGenerator

def perform_action_A(key, value):
    # 定义 A 操作的逻辑
    print(f"A操作: '{key}' 不被认为是敏感信息。")

def perform_action_B(question, key, value):
    # B操作：将问题中的 key 替换为 value
    new_question = re.sub(rf'\b{re.escape(key)}\b', value, question)
    print(f"B操作: 将 '{key}' 替换为 '{value}'。")
    return new_question

def extract_privacy_data(text):
    """提取文本中的隐私数据"""
    patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        'ip_address': r'(\d{1,3}\.){3}\d{1,3}',
        'credit_card': r'\b(?:\d{4}[-.\s]?){3}\d{4}\b',
        'location': r'\b\d+\.\d+\s*,\s*\d+\.\d+\b',
        'id_number': r'\b\d{6}-\d{4}\b',
        'social_security': r'\b\d{3}-\d{2}-\d{4}\b',
        'medical_record': r'\bMRN:\s*\d+\b',
    }

    extracted_data = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            extracted_data[key] = matches

    return extracted_data

def mask_partial(data, category):
    """根据类别进行部分掩码处理"""
    if category == 'email':
        return re.sub(r'(\w{1})[\w.-]+(@[\w.-]+)', r'\1****\2', data)
    elif category == 'phone':
        return re.sub(r'(\(?\d{3}\)?[-.\s]?)\d{3}([-.\s]?\d{4})', r'\1***\2', data)
    elif category == 'ip_address':
        return re.sub(r'(\d{1,3}\.\d{1,3}\.)\d{1,3}', r'\1***', data)
    elif category == 'credit_card':
        return re.sub(r'(\d{4}[-.\s]?){3}(\d{4})', r'****-****-****-\2', data)
    elif category in ['id_number', 'social_security']:
        return re.sub(r'(\d{3}-\d{2})-\d{4}', r'\1-****', data)
    elif category == 'medical_record':
        return re.sub(r'(MRN:\s*)\d+', r'\1****', data)
    else:
        return data  # 如果不匹配，不改变数据

def mask_and_replace(text, privacy_data, generator):
    """根据模型判断是否掩码并替换文本中的隐私数据"""
    masked_text = text  # 初始为原始文本

    for category, items in privacy_data.items():
        if items:  # 仅当有匹配项时处理
            for item in items:
                message = (
                    f"Determine if the following data '{item}' belongs to the category '{category}': "
                    "Please respond with 'Yes' or 'No'."
                )
                messages = [{"role": "user", "content": message}]
                response = generator.generate_text(messages, '')

                print(f"Response for '{item}': {response}")

                if "yes" in response.lower():
                    # 使用部分掩码替换
                    masked_item = mask_partial(item, category)
                    masked_text = masked_text.replace(item, masked_item)

    print("Encrypted new_question:", masked_text)  # 打印加密后的文本
    return masked_text


async def privacy_part(question):
    # 初始化加密器和生成器
    encryptor = get_encryptor()
    encrypted_text, replacement_dict = encryptor.encrypt_entities(question)
    # 去除相邻重复的隐私名称
    pattern = r'(<[^>]+>)(?:\s*<[^>]+>)+'
    encrypted_text = re.sub(pattern, r'\1', encrypted_text)

    print("Encrypted text:", encrypted_text)
    print("Entity replacement dictionary:", replacement_dict)
    new_question = question
    # 初始化文本生成器（同步调用）
    generator = TextGenerator(model_path="/home/zhaorh/code/ppagent/model/Llama-7B")  # 请将路径替换为实际模型路径

    # 遍历替换字典，逐项询问是否会影响任务解答
    for key, value in replacement_dict.items():
        message = (
            """Determine if the word "{key}" represents private data relevant to the task: {task}. 

### Private data may include:
 
1. **Personal names** related to individuals (such as user, recipient, or sender).
2. **Addresses or locations** tied to the user, recipient, or sender.
3. **Organizations or affiliations** connected with the user, recipient, or sender.

Consider whether the word "{key}" could be classified as personal or organizational information directly associated with someone involved in the context. 

If it aligns with the above categories, respond with **"Yes."** If it does not, respond with **"No."**
"""
        )

        # 填充 key 和 task

        message = message.format(key=key, task=question)
        # 将 message 包装为符合格式的列表
        messages = [{"role": "user", "content": message}]

        # 同步调用 generate_text，不使用 await
        response = generator.generate_text(messages, '')
        number_message = ("""
        """)
        print(f"Response for '{key}': {response}")
        if "yes" in response.lower():
            new_question = perform_action_B(new_question, key, value)  # B操作
        else:
            perform_action_A(key, value)  # A操作
    print(new_question)
    privacy_data = extract_privacy_data(new_question)
    # 输出处理后的隐私数据
    masked_new_question = mask_and_replace(new_question, privacy_data, generator)
    print(masked_new_question)


    return encrypted_text, replacement_dict,masked_new_question


