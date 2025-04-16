import json


def find_data_by_id(file_path, target_id):
    """
    从JSON文件中查找特定ID的数据并返回相关信息

    参数:
    file_path (str): JSON文件路径
    target_id (str): 要查找的ID

    返回:
    dict: 包含问题、答案、难度级别和所有上下文文本的字典
    """
    # 初始化一个变量用来存储找到的数据
    data_found = None
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            if item['id'] == target_id:
                data_found = item  # 将找到的数据赋值给data_found变量
                break

    if data_found is None:
        return None  # 如果没有找到数据，返回None

    # 提取问题、答案、难度级别
    result = {
        "Question": data_found['Question'],
        "Answer": data_found['Answer'],
        "Difficulty Level": data_found['Difficulty Level'],
        "All Context Texts": data_found['All Context Texts']
    }



    return result



