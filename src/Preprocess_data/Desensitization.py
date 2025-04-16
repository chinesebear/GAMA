from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re

class EntityEncryptor:
    def __init__(self, model_path, tokenizer_path, device=1):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.device = device

        # 加载模型和tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path)

        # 初始化NER pipeline
        self.nlp = pipeline("ner", model=self.model, tokenizer=self.tokenizer, device=self.device)

    def remove_subwords(self, entity_list):
        """去除实体中的冗余子串"""
        words = set(entity['word'] for entity in entity_list)
        words_to_remove = {word for word in words if any(word != other and word in other for other in words)}
        return [entity for entity in entity_list if entity['word'] not in words_to_remove]

    def long_entities(self, text):
        """处理长度超过512的文本"""
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        all_entities = []
        offset = 0

        for sentence in sentences:
            ner_results = self.nlp(sentence)
            for entity in ner_results:
                entity['start'] += offset
                entity['end'] += offset
                all_entities.append(entity)
            offset += len(sentence) + 1

        return all_entities

    def replace_and_record(self, text, ner_results, entity_type, placeholder_prefix, replacement_dict):
        """替换实体并记录替换关系"""
        unique_entities = {result['word'] for result in ner_results if result['entity'] == entity_type}
        for i, entity in enumerate(sorted(unique_entities), start=1):
            placeholder = f'<{placeholder_prefix}-{i}>'
            text = text.replace(entity, placeholder)
            replacement_dict[entity] = placeholder
        return text

    def encrypt_entities(self, text):
        """对文本进行实体加密"""
        tokens = text.split()
        if len(tokens) < 512:
            ner_results = self.nlp(text)
        else:
            print(f"文本大于512字符，共 {len(tokens)} 个token")
            ner_results = self.long_entities(text)

        ner_results = self.remove_subwords(ner_results)
        entities_to_remove = [r for r in ner_results if r['entity'].startswith(('I-ORG', 'I-PER', 'I-LOC'))]

        # 删除指定实体并调整文本
        for entity in sorted(entities_to_remove, key=lambda x: x['start'], reverse=True):
            before_entity = text[:entity['start']].rstrip()
            after_entity = text[entity['end']:].lstrip()
            text = before_entity + (' ' if before_entity and after_entity else '') + after_entity

        replacement_dict = {}
        text = self.replace_and_record(text, ner_results, 'B-PER', 'name', replacement_dict)
        text = self.replace_and_record(text, ner_results, 'B-LOC', 'location', replacement_dict)
        text = self.replace_and_record(text, ner_results, 'B-ORG', 'organization', replacement_dict)

        return text, replacement_dict



"""# 实例化类
model_path = "/home/zhaorh/code/ppagent//model/NER"
tokenizer_path = "/home/zhaorh/code/ppagent//model/NER"
entity_encryptor = EntityEncryptor(model_path, tokenizer_path)

# 测试加密功能
text = "John works at OpenAI in San Francisco."
encrypted_text, replacement_dict = entity_encryptor.encrypt_entities(text)

print("加密后的文本:", encrypted_text)
print("替换关系:", replacement_dict)"""
