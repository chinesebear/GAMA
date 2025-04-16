import numpy as np
#from src.Agents.memory import config_w2v
#config_w2v.initialize_calculator()
class SimilarityMatrixCalculator:
    def __init__(self, result, calculator):
        """
        :param result: 输入的领域词列表，形式如[('Entertainment', 'Extremely High'), ...]
        :param calculator: 相似度计算器实例
        """
        self.result = result
        self.calculator = calculator
        self.domains = ["Entertainment", "financial", "History", "legal", "Literature",
                        "medical", "Politics", "Sports", "technology", "science"]
        self.similarity_matrix = None

    def calculate_matrix(self):
        """
        计算相似度矩阵
        """
        self.similarity_matrix = np.zeros((len(self.result), len(self.domains)))

        for i, (word, _) in enumerate(self.result):
            # 如果 word 包含多个词，则选择每个词与目标词的最高相似度
            if ' ' in word:
                words = word.split()  # 将包含多个词的字符串分开
                max_similarity_dict = {}

                for w in words:
                    similarity = self.calculator.calculate_similarity(w)

                    if isinstance(similarity, dict):
                        for domain, score in similarity.items():
                            if score is None:
                                score = 0  # 将 None 设为 0
                            if domain not in max_similarity_dict or (score > max_similarity_dict[domain]):
                                max_similarity_dict[domain] = score
                    else:
                        print(f"Warning: Similarity value for '{w}' is not a dictionary. Using default value 0.")

                similarity = max_similarity_dict
            else:
                # 使用相似度计算器计算相似度
                similarity = self.calculator.calculate_similarity(word)

                if similarity is None:
                    similarity = {}  # 如果 similarity 为 None，则使用空字典

            # 检查返回的类型，并输出调试信息
            print(f"Similarity between {word} and domains: {similarity} (Type: {type(similarity)})")

            # 如果返回的是字典，提取每个领域的相似度值
            if isinstance(similarity, dict):
                for j, domain in enumerate(self.domains):
                    if domain in similarity:
                        self.similarity_matrix[i, j] = similarity[domain]
                    else:
                        print(
                            f"Warning: Domain '{domain}' not found in similarity dictionary for word '{word}'. Using default value 0.")
                        self.similarity_matrix[i, j] = 0
            else:
                # 如果返回的不是字典，抛出警告并使用默认值
                print(f"Warning: Similarity value for {word} is not a dictionary. Using default value 0.")
                self.similarity_matrix[i, :] = 0

        return self.similarity_matrix

    def return_matrix(self):
        """
        打印相似度矩阵
        """
        if self.similarity_matrix is not None:
            return self.similarity_matrix



"""
# 输入的领域词列表
result = [('Entertainment', 'Extremely High'), ('Music and it', 'High'), ('Animation or get', 'High')]

matrix_calculator = SimilarityMatrixCalculator(result, config_w2v.calculator)

# 计算并打印相似度矩阵
matrix_calculator.calculate_matrix()
similarity_matrix = matrix_calculator.return_matrix()
print(similarity_matrix)
"""
