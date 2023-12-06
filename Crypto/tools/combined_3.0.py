import itertools
from itertools import combinations, product
import time

# 假设 A, B, C, D, E, F, G 是布尔变量
A = True
B = False
C = True
D = False
E = True
F = False
G = True
H = False
I = True
J = False
K = False
L = True
M = False
N = True
O = False
P = True
Q = False
R = True
S = False
T = True
U = False
V = True
W = False
X = True
Y = False
Z = True

# 设置最多要取的条件数
buy_pool_number = 8
sell_pool_number = 8
buy_combined = 3
sell_combined = 3

# 定义一个函数来生成所有条件的组合，根据 combined_number 参数确定组合的最大长度
def generate_expressions(conditions, combined_number):
    expressions = []

    # 针对长度为 1 到 combined_number 的组合生成表达式
    for r in range(1, min(len(conditions), combined_number) + 1):
        for subset in combinations(conditions, r):
            if len(subset) == 1:
                expressions.append(subset[0])
            else:
                operators = list(product([' and ', ' or '], repeat=len(subset)-1))
                for operator in operators:
                    expr = ''
                    for i, cond in enumerate(subset):
                        expr += cond
                        if i < len(operator):
                            expr += operator[i]
                    expressions.append(expr)

    return expressions


buy_pool = [chr(i) for i in range(65, 65 + buy_pool_number)]
sell_pool = [chr(90 - i) for i in range(sell_pool_number)]
start_time = time.time()
buy_expression = generate_expressions(buy_pool, buy_combined)
sell_expression = generate_expressions(sell_pool, sell_combined)
expression_combinations = list(itertools.product(buy_expression, sell_expression))
end_time = time.time()
time_diff = end_time - start_time

# 打印组合数和执行时间
print(f"buy組合數: {len(buy_expression)} (buy_pool_number: {buy_pool_number}, buy_combined: {buy_combined})")
print(f"sell組合數: {len(sell_expression)} (sell_pool_number: {sell_pool_number}, sell_combined: {sell_combined})")
print(f"combined組合數: {len(expression_combinations)}")
print(f"執行時間：{time_diff} 秒")