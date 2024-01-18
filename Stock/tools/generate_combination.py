from itertools import combinations, product

# 定义一个函数来生成所有条件的组合
def with_combineNum(conditions, combined_number):
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

# 定义一个函数来生成所有条件的组合
def without_combineNum(conditions):
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