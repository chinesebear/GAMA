import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import os
import asyncio
import aiofiles

class TextDomainAnalyzer:
    def __init__(self):
        # 初始化停用词
        self.vectorizer = None
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """
        预处理给定文本：分词、转小写、移除非字母字符、过滤停用词。
        """
        words = nltk.word_tokenize(text)
        words = [word.lower() for word in words if word.isalpha()]
        words = [word for word in words if word not in self.stop_words]
        return ' '.join(words)

    async def domain_membership_score_normalized(self, text, domain):
        """
        计算文本相对于给定领域的归属分数。
        """
        # 文本预处理
        processed_text = self.preprocess_text(text)

        # 加载领域特定关键词
        keyword_file_path = f'../../data/field/{domain}_keywords.txt'
        if not os.path.exists(keyword_file_path):
            return domain, 0  # 如果文件不存在，返回0分

        async with aiofiles.open(keyword_file_path, 'r') as file:
            domain_keywords = await file.read()
            domain_keywords = [keyword.lower().strip() for keyword in domain_keywords.splitlines()]

        # 初始化向量化器
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit([processed_text] + domain_keywords)

        # 转换文本到TF-IDF矩阵
        tfidf_matrix = self.vectorizer.transform([processed_text]).toarray()

        # 计算领域关键词的TF-IDF分数
        domain_scores = [tfidf_matrix[0, self.vectorizer.vocabulary_.get(keyword)] for keyword in domain_keywords if
                         keyword in self.vectorizer.vocabulary_]
        total_domain_score = np.sum(domain_scores)

        # 计算所有词汇的总分数
        total_score = np.sum(tfidf_matrix[0])

        # 归一化领域得分
        normalized_score = total_domain_score / total_score if total_score > 0 else 0
        return domain, normalized_score
