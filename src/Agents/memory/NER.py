from src.Preprocess_data.Desensitization import EntityEncryptor

# 全局变量缓存 EntityEncryptor 实例
encryptor_instance = None

def get_encryptor():
    """获取 EntityEncryptor 实例。如果未初始化则初始化。"""
    global encryptor_instance
    if encryptor_instance is None:
        encryptor_instance = EntityEncryptor(
            model_path="/home/zhaorh/code/ppagent/model/NER",
            tokenizer_path="/home/zhaorh/code/ppagent/model/NER",
            device=1
        )
        print("EntityEncryptor initialized.")
    else:
        print("EntityEncryptor already initialized.")
    return encryptor_instance


