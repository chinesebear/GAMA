import json
import re

class FinalAnswerExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.contents = self.extract_contents_from_json()
        self.final_answers = self.extract_final_answers()

    def extract_contents_from_json(self):
        contents = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            file_content = re.sub(r'}\s*{', '},{', file_content)
            file_content = '[' + file_content + ']'
            try:
                data = json.loads(file_content)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                return []

            def recurse_extract(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key == 'content':
                            contents.append(value)
                        else:
                            recurse_extract(value)
                elif isinstance(data, list):
                    for item in data:
                        recurse_extract(item)

            recurse_extract(data)
        return contents

    def extract_final_answers(self):
        final_answers = []
        pattern = r'Final answer:(.+)'
        for content in self.contents:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                final_answers.extend([m.strip() for m in matches])
            else:
                print("No 'Final answer' found in content:", content)
        return final_answers

    def get_answer_by_index(self, index):
        if index - 1 < len(self.final_answers):
            return self.final_answers[index - 1]
        else:
            return "No answer available for this index"

# Usage


