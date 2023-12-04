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

# 创建一个包含 7 个条件的列表
# 设置最多要取的条件数
combined_number = 5
num_conditions = 5

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


# for combined_number in range(2, 14):
#     start_time = time.time()
#     expressions = generate_expressions(conditions, combined_number)
#     end_time = time.time()
#     time_diff = end_time - start_time
# # for expr in expressions:
# #     print(f"{expr}: {eval(expr)}")
#     # 打印组合数和执行时间
#     print(f"Combined number: {combined_number}, Number of expressions: {len(expressions)}, Execution time: {time_diff} seconds")

# # 以固定取 5 个条件的情况，测试条件总数从 5 到 15
# for num_conditions in range(5, 16):
#     # 创建一个包含 num_conditions 个条件的列表
#     conditions = [chr(i) for i in range(65, 65 + num_conditions)] # 使用 A, B, C, ... 作为条件名

#     # 固定最多要取的条件数为 5
#     combined_number = 5

#     start_time = time.time()
#     expressions = generate_expressions(conditions, combined_number)
#     end_time = time.time()
#     time_diff = end_time - start_time

#     # 打印组合数和执行时间
#     print(f"Total conditions: {num_conditions}, Number of expressions: {len(expressions)}, Execution time: {time_diff} seconds")
conditions = [chr(i) for i in range(65, 65 + num_conditions)]
start_time = time.time()
expressions = generate_expressions(conditions, combined_number)
end_time = time.time()
time_diff = end_time - start_time
# 打印组合数和执行时间
print(f"Total conditions: {num_conditions}, Combined number: {combined_number}, Number of expressions: {len(expressions)}, Execution time: {time_diff} seconds")