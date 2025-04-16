import json
import asyncio
from src.Agents.start_Q import QuestionProcessor

async def print_json_details(json_path):
    # 读取 JSONL 文件，每行一个 JSON 对象
    with open(json_path, 'r', encoding='utf-8') as file:
        id_ = 1
        for line in file:
            entry = json.loads(line)  # 解析每一行的 JSON 数据
            # 打印所需信息
            print('---')  # 分隔每个条目
            processor = QuestionProcessor()
            print("Processing question :", entry["idx"])
            print("Question:",entry["inputs"])
            # 注意这里使用 await
            answer = await processor.process_question(entry["inputs"],id_)
            id_ = id_+1
            print("finally answer IS:", answer)
            print(f'targets: {entry["targets"]}')

# 指定 JSON 文件的路径
json_path = '/mnt/c/workspace/code/xagent_zhao/data/logic_grid_puzzle/logic_grid_puzzle_200.jsonl'

# 运行异步函数
if __name__ == '__main__':
    asyncio.run(print_json_details(json_path))
