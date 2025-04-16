import asyncio
from src.Agents.roles.collector import QuestionCollector
from src.Agents.roles.expert_doing import ExpertCooperation
from src.Agents.roles.select_experter import ExpertSelector, IndustryExtractor
from src.text_analysis.word2vec_computer import SimilarityMatrixCalculator
from src.Agents.TF_expert import DomainScoreCalculator
from src.text_analysis.Google_text_analysis import  SimilarityCalculator
from src.Agents.memory import config_w2v
import numpy as np
def create_expert_sentence(expertise_areas):
    if not expertise_areas:
        return "You're an expert."

    # 构建基本句子
    expertise_sentence = "You are an expert in"

    # 遍历列表，添加每个领域的专家信息
    for i, (area, level) in enumerate(expertise_areas):
        if i == len(expertise_areas) - 1:  # 如果是最后一个元素，不添加逗号
            expertise_sentence += f" {area} with an {level} level of expertise."
        else:
            expertise_sentence += f" {area} with an {level} level of expertise, "

    return expertise_sentence





def find_max_domain(matrix, domains):
    max_domains = []

    for row in matrix:
        if np.any(row):  # 如果该行存在非零元素
            max_index = np.argmax(row)  # 找到每一行中最大值的位置
            max_domain = domains[max_index]  # 找到对应的领域
        else:
            max_domain = "none"  # 如果全为零，返回 'none'

        max_domains.append(max_domain)

    return max_domains

class ExpertPick:
    def __init__(self):
        pass



    async def process(self, question):
        try:
            # 收集问题相关信息
            collector = QuestionCollector()
            collected_information = await collector.collect(question)
            print(f"Collected Information: {collected_information}")

            # 增强问题
            enhanced_question = f"{question}: {collected_information}"
            print(f"Enhanced Question: {enhanced_question}")

            # 选择专家
            experts = ExpertSelector()
            expert_information = await experts.elector_expert(enhanced_question)
            print(f"Expert Information: {expert_information}")

            # 提取领域信息
            extractor = IndustryExtractor(expert_information)
            result = extractor.extract()
            print(f"Extracted Result: {result}")
            if  result:
                calculator_TF = DomainScoreCalculator()

                # 打印领域归属分数
                domain_scores = await calculator_TF.get_domain_scores(question)
                for domain, score in domain_scores.items():
                    print(f"Domain: {domain}, Normalized Score: {score:.4f}")
                scores = list(domain_scores.values())

                # 假设config_w2v已经有一个calculator实例，带有calculate_similarity方法

                matrix_calculator = SimilarityMatrixCalculator(result, config_w2v.calculator)

                # 计算并打印相似度矩阵
                matrix_calculator.calculate_matrix()
                similarity_matrix=matrix_calculator.return_matrix()
                similarity_matrix = np.nan_to_num(similarity_matrix, nan=0)
                print(similarity_matrix)
                TF_matrix = np.broadcast_to(scores, similarity_matrix.shape)
                TF_w2v_matrix =(0.95*similarity_matrix) +(0.05*TF_matrix)


                domains = ["Entertainment", "financial", "History", "legal", "Literature",
                           "medical", "Politics", "Sports", "technology", "science"]

                # 找出每一行中最大值对应的领域
                expert_field = find_max_domain(TF_w2v_matrix, domains)
                print(expert_field)
                new_result = [(expert_field[i], description) for i, (_, description) in enumerate(result)]
                print('new',new_result)
                filtered_data = [item for item in new_result if item[0] != 'none']
                filtered_data = [item for item in filtered_data if item[0].lower() != 'none' and 'low' not in item[1].lower()]
                merged_data = {}
                for item in filtered_data:
                    domain, score = item
                    if domain not in merged_data:
                        merged_data[domain] = score

                # 转换为最终结果列表
                final_data = list(merged_data.items())

                sentence = create_expert_sentence(final_data)
            else:
                sentence = "You're an expert."
            return sentence, final_data
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

