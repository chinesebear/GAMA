import numpy as np
import matplotlib.pyplot as plt

# 定义高斯函数
def gaussian(x, mu, sigma):
    return 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - mu)**2 / (2 * sigma**2))

# 优化函数以改善标签位置，不让其影响到函数曲线
def plot_gaussians_with_optimized_labels(input_x):
    # 生成x值
    x = np.linspace(0, 1, 1000)

    # 定义标准差
    sigma = 0.05

    # 计算七个不同中点的高斯函数的y值
    y1 = gaussian(x, mu=0.1, sigma=sigma)
    y2 = gaussian(x, mu=0.2, sigma=sigma)
    y3 = gaussian(x, mu=0.3, sigma=sigma)
    y4 = gaussian(x, mu=0.4, sigma=sigma)
    y5 = gaussian(x, mu=0.5, sigma=sigma)
    y6 = gaussian(x, mu=0.6, sigma=sigma)
    y7 = gaussian(x, mu=0.8, sigma=sigma)

    # 生成七个高斯函数在输入x值处的y值
    y_values_at_input = [
        gaussian(input_x, mu=0.1, sigma=sigma),
        gaussian(input_x, mu=0.2, sigma=sigma),
        gaussian(input_x, mu=0.3, sigma=sigma),
        gaussian(input_x, mu=0.4, sigma=sigma),
        gaussian(input_x, mu=0.5, sigma=sigma),
        gaussian(input_x, mu=0.6, sigma=sigma),
        gaussian(input_x, mu=0.8, sigma=sigma)
    ]

    # 绘制图像
    plt.figure(figsize=(10, 5))
    plt.plot(x, y1, label='Mean 0.1')
    plt.plot(x, y2, label='Mean 0.2')
    plt.plot(x, y3, label='Mean 0.3')
    plt.plot(x, y4, label='Mean 0.4')
    plt.plot(x, y5, label='Mean 0.5')
    plt.plot(x, y6, label='Mean 0.6')
    plt.plot(x, y7, label='Mean 0.8')

    # 标出七个点
    plt.scatter([input_x]*7, y_values_at_input, color='red')
    for i, y_val in enumerate(y_values_at_input):
        plt.text(input_x, y_val, f'{y_val:.2f}', horizontalalignment='right', verticalalignment='bottom')

    plt.title('Optimized Gaussian Functions with Labels Not Affecting the Curves')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()

    # 确定最大y值对应的曲线
    max_y_index = y_values_at_input.index(max(y_values_at_input))
    membership = ["Extremely Low", "Low", "Moderately Low", "Medium", "Moderately High", "High", "Extremely High"][max_y_index]

    # 返回隶属度描述
    return membership

# 使用示例
membership = plot_gaussians_with_optimized_labels(0.5)  # 输入x值
print("Membership at x =", 0.5, "is:", membership)


