from itertools import product

# 定义一个函数来生成所有条件的组合，固定一个条件
def generate_expressions(conditions, fixed_condition):
    expressions = []
    
    # 从条件列表中移除固定条件
    other_conditions = [cond for cond in conditions if cond != fixed_condition]
    
    # 当固定条件为空时，直接将条件添加到表达式列表
    if fixed_condition == '':
        expressions.extend(other_conditions)
    else:
        # 生成固定条件与其他条件的 'and' 和 'or' 组合
        for cond in other_conditions:
            for operator in [' and ', ' or ']:
                expr = fixed_condition + operator + cond
                expressions.append(expr)

    return expressions

# 示例用法
conditions = ['A', 'B', 'C', 'D']
fixed_condition = ''
expressions = generate_expressions(conditions, fixed_condition)
for expr in expressions:
    print(expr)
