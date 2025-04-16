from transformers import BertTokenizer, BertModel
import os

def download_bert_model(model_name="bert-base-uncased", save_directory="./EV_NER"):
    # 创建保存目录（如果不存在）
    os.makedirs(save_directory, exist_ok=True)

    # 加载分词器
    tokenizer = BertTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(save_directory)  # 保存分词器到指定目录

    # 加载模型
    model = BertModel.from_pretrained(model_name)
    model.save_pretrained(save_directory)  # 保存模型到指定目录

if __name__ == "__main__":
    download_bert_model(save_directory="/home/zhaorh/code/ppagent/model")
