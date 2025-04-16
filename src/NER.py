from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json
import torch
local_model_path = "/home/yang/home/yang/workspace/code/xagent/model/NER"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForTokenClassification.from_pretrained(local_model_path)
model.to(device)

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def find_nth_word_position(sentence, n):
    """
    Find the position of the nth word in a sentence.

    Parameters:
    sentence (str): The sentence in which to search for the word.
    n (int): The position of the word to find (1-based indexing).

    Returns:
    int: The starting index of the nth word in the sentence, or -1 if not found.
    """
    words = sentence.split()  # Split the sentence into words

    if n > len(words) or n < 1:  # Check if the request is out of bounds
        return -1  # Return -1 if the nth word doesn't exist

    # Find the start position of the nth word
    start_position = sum(len(word) + 1 for word in words[:n - 1])

    return start_position

# 模拟模型处理函数
def process_context(context):
    # 这里可以是你调用模型的代码，对context进行处理
    # 替换成你的实际处理逻辑
    processed_result = context
    return processed_result

TP = 0
FN = 0
TN = 0
FP = 0
# 读取测试集文件
with open('/home/yang/home/yang/workspace/code/xagent/doc/mrc-ner.test', 'r', encoding='utf-8') as file:
    test_set = json.load(file)

# 对每个样本进行处理并输出结果
for sample in test_set:
    qas_id = sample["qas_id"]
    contexts = sample["context"]
    processed_context = process_context(contexts)
    print("例子")
    print(sample)
    # 输出结果


    ner_results = nlp(processed_context)
    print("处理后")
    print(ner_results)
    if not sample['impossible']:
        # 检查是否有符合条件的entity
        entity_found = False
        for ner_result in ner_results:
            print("内容,NER")
            print(ner_result)
            if ner_result['entity'] in ['B-' + sample['entity_label'], 'I-' + sample['entity_label']]:
                print("结果有有有有有有有有有有有有有有有有有有有")
                print(find_nth_word_position(sample['context'],sample['start_position'][0]))
                print(ner_result['start'])
                if len(sample['start_position']) > 0 and find_nth_word_position(sample['context'],sample['start_position'][0]+1) == ner_result['start']:
                    entity_found = True
                    break
                elif len(sample['start_position']) > 1 and find_nth_word_position(sample['context'],sample['start_position'][1]+1) == ner_result['start']:
                    entity_found = True
                    break
        if entity_found:
            TP += 1
        if not entity_found:
            FN += 1
    else:
        # 检查是否有不应存在的entity
        entity_found = False
        for ner_result in ner_results:
            if ner_result['entity'] in ['B-' + sample['entity_label'], 'I-' + sample['entity_label']]:
                FP += 1
                entity_found = True
                break
        if not entity_found:
            TN += 1

    # 输出结果
    print(f"TP: {TP}, FN: {FN}, FP: {FP}, TN: {TN}")


















