from itertools import combinations, product

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

# 创建一个包含 10 个条件的列表
conditions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

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
expressions = generate_expressions(conditions)
for expr in expressions:
    # 执行每个表达式并打印结果
    print(f"{expr}: {eval(expr)}")

# 打印最终的计数
print(len(expressions))
