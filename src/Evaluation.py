from transformers import BertTokenizer, BertModel
import torch
from nltk.translate.bleu_score import sentence_bleu




import re
# 初始化 BERT 模型和分词器
tokenizer = BertTokenizer.from_pretrained('/home/zhaorh/code/ppagent/model/bert-base-uncased')
model = BertModel.from_pretrained('/home/zhaorh/code/ppagent/model/bert-base-uncased')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def cosine_similarity(embedding1, embedding2):
    return torch.nn.functional.cosine_similarity(embedding1, embedding2).item()

def calculate_f1(hidden_count, total_hidden, non_hidden_count, total_non_hidden):
    precision = hidden_count / total_hidden if total_hidden > 0 else 0
    recall = hidden_count / non_hidden_count if non_hidden_count > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1

def evaluate_bleu(original_text, masked_text):
    reference = original_text.split()
    candidate = masked_text.split()
    return sentence_bleu([reference], candidate)

def evaluate_semantic_similarity(original_text, masked_text):
    embedding_original = get_embedding(original_text)
    embedding_masked = get_embedding(masked_text)
    return cosine_similarity(embedding_original, embedding_masked)

def evaluate_f1(hidden_privacy_count, total_privacy_count, non_privacy_count, false_hidden_count):
    return calculate_f1(hidden_privacy_count, total_privacy_count, non_privacy_count, false_hidden_count)


def update_privacy_scores(scores, scores_2, text, privacy_data):
    """
    根据文本内容和隐私数据更新分数，记录未匹配的隐私项数量。

    参数：
    - scores: 更新后的分数字典，记录未匹配的隐私项数量
    - scores_2: 统计每类隐私项的总数
    - text: 要检测的文本内容（可能已被加密）
    - privacy_data: 包含隐私数据的字典结构

    返回：
    - 更新后的 scores 和 scores_2 字典
    """
    # 检查参数类型
    if not isinstance(text, str):
        raise ValueError("输入的文本（text）必须是字符串类型")
    if not isinstance(privacy_data, dict):
        raise ValueError("隐私数据（privacy_data）必须是字典类型")

    matched_items = set()  # 记录已匹配的隐私项

    # 遍历每一类隐私数据
    for category, items in privacy_data.items():
        # 确保 scores_2 累加该类别的总数
        if category not in scores_2:
            scores_2[category] = 0
        scores_2[category] += len(items)

        # 初始化该类别的分数，如果不存在则置为 0
        if category not in scores:
            scores[category] = 0

        # 遍历该类别的每一个数据项
        for item in items:
            # 检查 item 是否是字符串类型
            if not isinstance(item, str) or not item.strip():
                print(f"跳过无效数据项：{item} 在类别：{category}")
                continue

            try:
                # 使用正则表达式匹配，忽略大小写和空格差异
                pattern = re.compile(re.escape(item.strip()), re.IGNORECASE)
                if not pattern.search(text):
                    scores[category] += 1  # 未匹配到则计数加 1
                    print(f"未匹配到：{item} 在类别：{category}")
                else:
                    print(f"匹配到：{item} 在类别：{category}")
            except re.error as e:
                print(f"正则表达式错误：{e}，跳过数据项：{item}")

    return scores, scores_2




def count_non_privacy_words(text, privacy_data):
    """
    统计文本中除了隐私数据外的其它单词数量。

    参数：
    - text: 输入的文本字符串。
    - privacy_data: 包含隐私数据的字典。

    返回：
    - 非隐私单词的数量。
    """

    # 使用正则表达式提取文本中的所有单词
    words = re.findall(r'\b\w+\b', text)

    # 将所有隐私数据项收集到一个集合中
    privacy_words = set()
    for category, items in privacy_data.items():
        privacy_words.update(items)

    # 过滤掉隐私数据中的单词
    non_privacy_words = [word for word in words if word not in privacy_words]

    # 返回非隐私单词的数量
    return len(non_privacy_words)

def count_nested_answers_in_text(text, nested_answers):
    """
    计算文本中包含给定答案字典中答案的个数。
    每个子列表视为一个单独的得分单位，如果文本包含子列表中的任何一个答案，则得分加一。
    使用正则表达式确保匹配完整单词边界，并处理数字后缀（如 "12th" 匹配 "12"）。

    参数:
    - text (str): 需要检查的文本。
    - nested_answers (dict): 嵌套答案字典，每个键对应一个问题，值为包含多个可能答案的列表。

    返回:
    - int: 总得分。
    """
    lower_text = text.lower()  # 将文本转换为小写，方便匹配
    total_score = 0  # 初始化总得分
    answer_index = 1  # 用于标识当前答案编号

    # 遍历每个问题的答案列表
    for key, answers in nested_answers.items():
        found = False  # 标识是否在当前问题中找到匹配答案

        # 遍历该问题的所有可能答案
        for answer_set in answers:
            words = answer_set.lower().split()  # 拆分答案为单词列表

            # 检查答案中的所有单词是否都能在文本中找到
            if all(re.search(r'\b' + re.escape(word) + r'[a-z]*s?\b', lower_text) for word in words):
                # 如果答案包含数字，处理数字后缀
                if any(word.isdigit() for word in words):
                    if all(re.search(r'\b' + re.escape(word) + r'(?:st|nd|rd|th)?\b', lower_text) for word in words):
                        print(f'The {answer_index} correct answer is identified. The correct answer is {answer_set}')
                        found = True
                        break
                else:
                    print(f'The {answer_index} correct answer is identified. The correct answer is {answer_set}')
                    found = True
                    break

        if found:
            total_score += 1
        else:
            print(
                f'The correct answer was not identified for the {answer_index} one, and the solution does not have the following answer: {answers}')

        answer_index += 1  # 增加答案编号

    return total_score



def extract_words(text):
    """从文本中提取所有单词，将连字符拆分为多个单词。"""
    # 将连字符替换为空格，然后提取单词
    text = text.replace('-', ' ')
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)



def filter_privacy_words(words, privacy_data):
    """从单词集合中排除隐私数据中的词汇。"""
    privacy_words = set()
    for category, items in privacy_data.items():
        privacy_words.update(item.lower() for item in items)  # 将所有隐私词汇转换为小写
    return words - privacy_words  # 返回去除隐私词汇后的集合

def count_missing_words(text1, text2, privacy_data):
    """
    统计 text1 中在 text2 中未出现的单词个数（排除隐私数据）。

    参数：
    - text1: 原始文本。
    - text2: 用于比较的文本。
    - privacy_data: 隐私数据字典。

    返回：
    - 未出现在 text2 中的单词数量。
    - 未出现在 text2 中的单词列表。
    """
    # 提取两个文本的单词集合
    words1 = extract_words(text1)
    words2 = extract_words(text2)

    # 从单词集合中排除隐私数据词汇
    words1_filtered = filter_privacy_words(words1, privacy_data)
    words2_filtered = filter_privacy_words(words2, privacy_data)

    # 找出 text1 中不在 text2 中的单词
    missing_words = words1_filtered - words2_filtered

    # 返回未出现单词的数量和列表
    return len(missing_words), missing_words



def process_privacy_scores_and_metrics(
    scores_ner, scores_2_ner,
    scores_llm, scores_2_llm,
    scores_mask, scores_2_mask,
    NER_question, LLM_masked_question, masked_question,
    data, task_all,
    ner_bleu_scores, ner_semantic_similarities,
    llm_bleu_scores, llm_semantic_similarities,
    mask_bleu_scores, mask_semantic_similarities,
    missing_count_ner_sum, non_privacy_count_ner_sum,
    missing_count_llm_sum, non_privacy_count_llm_sum,
    missing_count_mask_sum, non_privacy_count_mask_sum
):
    # 更新隐私得分
    scores_ner, scores_2_ner = update_privacy_scores(scores_ner, scores_2_ner, NER_question, data.get('privacy_data'))
    scores_llm, scores_2_llm = update_privacy_scores(scores_llm, scores_2_llm, LLM_masked_question, data.get('privacy_data'))
    scores_mask, scores_2_mask = update_privacy_scores(scores_mask, scores_2_mask, masked_question, data.get('privacy_data'))

    # 计算非隐私词的数量
    non_privacy_count_ner = count_non_privacy_words(NER_question, data.get('privacy_data'))
    non_privacy_count_llm = count_non_privacy_words(LLM_masked_question, data.get('privacy_data'))
    non_privacy_count_mask = count_non_privacy_words(masked_question, data.get('privacy_data'))

    # 计算丢失的词数量和列表
    missing_count_ner, missing_words_ner = count_missing_words(task_all, NER_question, data.get('privacy_data'))
    missing_count_llm, missing_words_llm = count_missing_words(task_all, LLM_masked_question, data.get('privacy_data'))
    missing_count_mask, missing_words_mask = count_missing_words(task_all, masked_question, data.get('privacy_data'))

    # 评估 BLEU 和语义相似度
    bleu_score_ner = evaluate_bleu(task_all, NER_question)
    semantic_similarity_ner = evaluate_semantic_similarity(task_all, NER_question)
    ner_bleu_scores.append(bleu_score_ner)
    ner_semantic_similarities.append(semantic_similarity_ner)

    bleu_score_llm = evaluate_bleu(task_all, LLM_masked_question)
    semantic_similarity_llm = evaluate_semantic_similarity(task_all, LLM_masked_question)
    llm_bleu_scores.append(bleu_score_llm)
    llm_semantic_similarities.append(semantic_similarity_llm)

    bleu_score_mask = evaluate_bleu(task_all, masked_question)
    semantic_similarity_mask = evaluate_semantic_similarity(task_all, masked_question)
    mask_bleu_scores.append(bleu_score_mask)
    mask_semantic_similarities.append(semantic_similarity_mask)

    # 打印结果
    print("ner", bleu_score_ner, semantic_similarity_ner,
          "llm", bleu_score_llm, semantic_similarity_llm,
          "mask", bleu_score_mask, semantic_similarity_mask)

    # 累加统计结果
    missing_count_ner_sum += missing_count_ner
    non_privacy_count_ner_sum += non_privacy_count_ner
    missing_count_llm_sum += missing_count_llm
    non_privacy_count_llm_sum += non_privacy_count_llm
    missing_count_mask_sum += missing_count_mask
    non_privacy_count_mask_sum += non_privacy_count_mask

    # 返回所有更新后的变量
    return (
        scores_ner, scores_2_ner,
        scores_llm, scores_2_llm,
        scores_mask, scores_2_mask,
        ner_bleu_scores, ner_semantic_similarities,
        llm_bleu_scores, llm_semantic_similarities,
        mask_bleu_scores, mask_semantic_similarities,
        missing_count_ner_sum, non_privacy_count_ner_sum,
        missing_count_llm_sum, non_privacy_count_llm_sum,
        missing_count_mask_sum, non_privacy_count_mask_sum
    )



def calculate_and_print_metrics(
    scores_ner, scores_2_ner, missing_count_ner_sum, non_privacy_count_ner_sum,
    scores_llm, scores_2_llm, missing_count_llm_sum, non_privacy_count_llm_sum,
    scores_mask, scores_2_mask, missing_count_mask_sum, non_privacy_count_mask_sum,
    ner_bleu_scores, ner_semantic_similarities,
    llm_bleu_scores, llm_semantic_similarities,
    mask_bleu_scores, mask_semantic_similarities
):
    try:
        def weighted_metrics(hidden_count, total_privacy, false_hidden, non_privacy_count):
            print('计算F1的',hidden_count, total_privacy, false_hidden, non_privacy_count)
            # 计算隐私类的Precision、Recall和F1
            if hidden_count + false_hidden > 0:
                precision_privacy = hidden_count / (hidden_count + false_hidden)
            else:
                precision_privacy = 0.0

            if total_privacy > 0:
                recall_privacy = hidden_count / total_privacy
            else:
                recall_privacy = 0.0

            if precision_privacy + recall_privacy > 0:
                f1_privacy = 2 * precision_privacy * recall_privacy / (precision_privacy + recall_privacy)
            else:
                f1_privacy = 0.0

            # 计算非隐私类的Precision、Recall和F1
            if non_privacy_count > 0:
                precision_non_privacy = (non_privacy_count - false_hidden) / non_privacy_count
                recall_non_privacy = (non_privacy_count - false_hidden) / non_privacy_count
            else:
                precision_non_privacy = 0.0
                recall_non_privacy = 0.0

            if precision_non_privacy + recall_non_privacy > 0:
                f1_non_privacy = 2 * precision_non_privacy * recall_non_privacy / (
                            precision_non_privacy + recall_non_privacy)
            else:
                f1_non_privacy = 0.0

            # 计算权重
            total_count = total_privacy + non_privacy_count
            weight_privacy = total_privacy / total_count if total_count > 0 else 0.0
            weight_non_privacy = non_privacy_count / total_count if total_count > 0 else 0.0

            # 加权Precision、Recall和F1
            weighted_precision = (precision_privacy * weight_privacy) + (precision_non_privacy * weight_non_privacy)
            weighted_recall = (recall_privacy * weight_privacy) + (recall_non_privacy * weight_non_privacy)
            if weighted_precision + weighted_recall > 0:
                weighted_f1 = 2 * weighted_precision * weighted_recall / (weighted_precision + weighted_recall)
            else:
                weighted_f1 = 0.0

            return weighted_precision, weighted_recall, weighted_f1

        # 计算 NER 指标
        hidden_privacy_count_ner = sum(scores_ner.values())
        total_privacy_count_ner = sum(scores_2_ner.values())
        false_hidden_count_ner = missing_count_ner_sum
        non_privacy_count_ner = non_privacy_count_ner_sum

        # 计算 LLM 指标
        hidden_privacy_count_llm = sum(scores_llm.values())
        total_privacy_count_llm = sum(scores_2_llm.values())
        false_hidden_count_llm = missing_count_llm_sum
        non_privacy_count_llm = non_privacy_count_llm_sum

        # 计算 Mask 指标
        hidden_privacy_count_mask = sum(scores_mask.values())
        total_privacy_count_mask = sum(scores_2_mask.values())
        false_hidden_count_mask = missing_count_mask_sum
        non_privacy_count_mask = non_privacy_count_mask_sum

        # 打印并计算 NER 评估指标
        print("NER Metrics:")
        precision_ner, recall_ner, f1_ner = weighted_metrics(
            hidden_privacy_count_ner, total_privacy_count_ner,
            false_hidden_count_ner, non_privacy_count_ner
        )
        print(f"  Precision: {precision_ner:.3f}")
        print(f"  Recall: {recall_ner:.3f}")
        print(f"  F1 Score: {f1_ner:.3f}")
        print("-" * 50)

        # 打印并计算 LLM 评估指标
        print("LLM Metrics:")
        precision_llm, recall_llm, f1_llm = weighted_metrics(
            hidden_privacy_count_llm, total_privacy_count_llm,
            false_hidden_count_llm, non_privacy_count_llm
        )
        print(f"  Precision: {precision_llm:.3f}")
        print(f"  Recall: {recall_llm:.3f}")
        print(f"  F1 Score: {f1_llm:.3f}")
        print("-" * 50)

        # 打印并计算 Mask 评估指标
        print("Mask Metrics:")
        precision_mask, recall_mask, f1_mask = weighted_metrics(
            hidden_privacy_count_mask, total_privacy_count_mask,
            false_hidden_count_mask, non_privacy_count_mask
        )
        print(f"  Precision: {precision_mask:.3f}")
        print(f"  Recall: {recall_mask:.3f}")
        print(f"  F1 Score: {f1_mask:.3f}")
        print("-" * 50)

        # 计算并打印 BLEU 和语义相似度
        bleu_ner = sum(ner_bleu_scores) / len(ner_bleu_scores)
        similarity_ner = sum(ner_semantic_similarities) / len(ner_semantic_similarities)

        bleu_llm = sum(llm_bleu_scores) / len(llm_bleu_scores)
        similarity_llm = sum(llm_semantic_similarities) / len(llm_semantic_similarities)

        bleu_mask = sum(mask_bleu_scores) / len(mask_bleu_scores)
        similarity_mask = sum(mask_semantic_similarities) / len(mask_semantic_similarities)

        print("\nNER Evaluation:")
        print(f"  BLEU Score: {bleu_ner:.3f}")
        print(f"  Semantic Similarity: {similarity_ner:.3f}")

        print("\nLLM Evaluation:")
        print(f"  BLEU Score: {bleu_llm:.3f}")
        print(f"  Semantic Similarity: {similarity_llm:.3f}")

        print("\nMASK Evaluation:")
        print(f"  BLEU Score: {bleu_mask:.3f}")
        print(f"  Semantic Similarity: {similarity_mask:.3f}")

    except Exception as e:
        print(f"An error occurred: {e}")
