import asyncio
from src.text_analysis.TF_IDF import TextDomainAnalyzer

class DomainScoreCalculator:
    def __init__(self):
        """
        初始化类，创建 TextDomainAnalyzer 实例，并定义领域列表。
        """
        self.analyzer = TextDomainAnalyzer()
        self.domains = ["Entertainment", "financial", "History", "legal", "Literature",
                        "medical", "Politics", "Sports", "technology", "science"]

    async def calculate_domain_scores(self, sample_text):
        """
        计算给定文本在各个领域的归属分数。

        参数:
        - sample_text: 要计算的文本。

        返回:
        - 一个字典，键是领域名称，值是归属分数。
        """
        domain_scores = {}

        # 逐个领域计算归属分数
        for domain in self.domains:
            result = await self.analyzer.domain_membership_score_normalized(sample_text, domain)
            domain_scores[result[0]] = result[1]

        return domain_scores

    async def get_domain_scores(self, sample_text):
        """
        计算并返回每个领域的归属分数。

        参数:
        - sample_text: 要计算的文本。

        返回:
        - 一个字典，包含每个领域的归属分数。
        """
        domain_scores = await self.calculate_domain_scores(sample_text)
        return domain_scores
