def weighted_metrics(hidden_count, total_privacy, false_hidden, non_privacy_count):
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
        f1_non_privacy = 2 * precision_non_privacy * recall_non_privacy / (precision_non_privacy + recall_non_privacy)
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

# 定义输入数据
datasets = {
    "NER": {
        "hidden_count": 405,
        "total_privacy": 500,
        "false_hidden": 1995,
        "non_privacy_count": 12626,
    },
    "LLM": {
        "hidden_count": 500,
        "total_privacy": 500,
        "false_hidden": 1190,
        "non_privacy_count": 13119,
    },
    "Mask": {
        "hidden_count": 468,
        "total_privacy": 500,
        "false_hidden": 632,
        "non_privacy_count": 13158,
    },
}

# 计算并打印结果
for dataset_name, metrics in datasets.items():
    weighted_precision, weighted_recall, weighted_f1 = weighted_metrics(
        metrics["hidden_count"],
        metrics["total_privacy"],
        metrics["false_hidden"],
        metrics["non_privacy_count"]
    )
    print(f"{dataset_name} Metrics:")
    print(f"  Weighted Precision: {weighted_precision:.4f}")
    print(f"  Weighted Recall: {weighted_recall:.4f}")
    print(f"  Weighted F1 Score: {weighted_f1:.4f}")
    print("-" * 50)
