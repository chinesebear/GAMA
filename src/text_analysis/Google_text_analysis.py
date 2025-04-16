

from concurrent.futures import ThreadPoolExecutor
from gensim.models import KeyedVectors
from nltk.tokenize import word_tokenize
import numpy as np


class SimilarityCalculator:
    def __init__(self):
        """
        初始化类，加载预训练的词向量模型，并设置目标词列表。

        参数:
        - model_path: 预训练模型的路径 (例如 Google News Word2Vec 模型)。
        - target_words: 需要计算相似度的目标词列表。
        """
        self.model_path = '/mnt/c/workspace/code/xagent_zhao_Llama3/model/gensim-data/word2vec-google-news-300/word2vec-google-news-300/GoogleNews-vectors-negative300.bin'
        self.target_words = ["Entertainment", "financial", "History", "legal", "Literature", "medical", "Politics", "Sports",
                        "technology", "science"]
        # 加载预训练的 Word2Vec 模型
        self.model = KeyedVectors.load_word2vec_format(self.model_path, binary=True)
        self.model.fill_norms()

        # 设置目标词列表
        self.target_words = self.target_words

    def preprocess_text(self, text):
        """
        预处理文本，将句子分解为单词。

        参数:
        - text: 输入文本，可能是一个词或一个句子。

        返回:
        - 分词后的单词列表。
        """
        words = word_tokenize(text.lower())
        return [word for word in words if word.isalpha()]

    def calculate_similarity(self, word_or_sentence):
        """
        计算一个词或句子与目标词列表中每个词的相似度分数。

        参数:
        - word_or_sentence: 输入，可以是一个词或一个句子。

        返回:
        - 一个字典，包含每个目标词与输入词/句的最高相似度。
        """
        try:
            # 预处理输入，将句子或词分解为单词
            words = self.preprocess_text(word_or_sentence)

            # 初始化相似度结果
            similarity_scores = {}

            # 使用并行计算
            with ThreadPoolExecutor() as executor:
                # 创建任务列表，针对每个目标词执行并行计算
                future_to_target = {executor.submit(self._calculate_max_similarity, words, target_word): target_word for
                                    target_word in self.target_words}

                # 获取结果并存入 similarity_scores 字典
                for future in future_to_target:
                    target_word = future_to_target[future]
                    try:
                        max_similarity = future.result()
                        similarity_scores[target_word] = max_similarity
                    except Exception as e:
                        print(f"Error calculating similarity for '{target_word}': {e}")
                        similarity_scores[target_word] = None

            return similarity_scores

        except Exception as e:
            print(f"An error occurred while calculating similarity:{e}")
            return None

    def _calculate_max_similarity(self, words, target_word):
        """
        辅助函数，计算输入词列表中与目标词的最高相似度。

        参数:
        - words: 输入词列表（句子切分后的词）。
        - target_word: 目标词。

        返回:
        - 输入词列表与目标词的最高相似度。
        """
        if target_word not in self.model.key_to_index:
            print(f"Target word '{target_word}' is not in vocabulary and has been skipped.")
            return None

        max_similarity = 0
        for w in words:
            if w in self.model.key_to_index:
                similarity = self.model.similarity(w, target_word)
                if similarity > max_similarity:
                    max_similarity = similarity
            else:
                print(f"The word '{w}' is not in the vocabulary and has been skipped.")

        return max_similarity if max_similarity > 0 else None


