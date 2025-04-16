from src.LLM_Model.Llama_8B import TextGenerator


# 全局变量缓存 TextGenerator 实例
generator_instance = None

def get_generator(model_path="/home/zhaorh/code/ppagent/model/Llama-7B"):
    """获取 TextGenerator 实例。如果未初始化则初始化。"""
    global generator_instance
    if generator_instance is None:
        generator_instance = TextGenerator(model_path)
        print("TextGenerator initialized.")
    else:
        print("TextGenerator already initialized.")
    return generator_instance