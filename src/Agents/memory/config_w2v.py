from src.text_analysis.Google_text_analysis import SimilarityCalculator

calculator = None  # 全局变量

def initialize_calculator():
    """初始化 calculator 变量"""
    global calculator
    if calculator is None:
        calculator = SimilarityCalculator()
        print(" Word2vec Calculator initialized.")
    else:
        print("Calculator already initialized.")