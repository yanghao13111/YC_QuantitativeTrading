from itertools import combinations, product
import itertools
import time

# 假设 A, B, C, ..., J 是布尔变量
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

# 创建一个包含 10 个条件的列表
buy_pool = ['A', 'B', 'C', 'D']
sell_pool = ['D', 'E', 'F', 'G', 'N']

# 定义一个函数来生成所有条件的组合
def generate_expressions(conditions):
    expressions = []

    # 针对不同长度的组合生成表达式
    for r in range(1, len(conditions) + 1):
        for subset in combinations(conditions, r):
            # 对于每个子集，生成所有可能的 AND/OR 组合
            operators = list(product([' and ', ' or '], repeat=r-1))
            for operator in operators:
                expr = ''
                for i, cond in enumerate(subset):
                    expr += cond
                    if i < len(operator):
                        expr += operator[i]
                expressions.append(expr)

    return expressions

# 生成并打印表达式
# 测试 generate_expressions2
start_time = time.time()
buy_expression = generate_expressions(buy_pool)
sell_expression = generate_expressions(sell_pool)
expression_combinations = list(itertools.product(buy_expression, sell_expression))
end_time = time.time()
for buy_expr, sell_expr in expression_combinations:
    # 执行每个表达式并打印结果
    print(f"{buy_expr}: {eval(buy_expr)} & {sell_expr}: {eval(sell_expr)}")

# 打印最终的计数
print(f"buy組合數{len(buy_expression)} sell組合數{len(sell_expression)} combined組合數{len(expression_combinations)}")
print(f"執行時間：{end_time - start_time} 秒")
