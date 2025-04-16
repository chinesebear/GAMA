import json

def extract_ids(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        id_list = [item['id'] for item in data]
    return id_list

