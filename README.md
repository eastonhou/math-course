# math-course
# 常见参数及生成器说明：
- level: 决定系数的复杂度，数值越大，计算量越大，建议加减法从0开始，乘除法从1开始
- generate_ranged: 生成限定范围的常数
- generate_factored: 生成限定因子数的常数
- 一般来说，涉及乘除或分数运算的，用generate_factored，以避免因子中出现大素数因子，不易化简
# 生成器构造方法：Generator(prime_numbers, prime_factors, maxinum, signed)
- prime_numbers: 素因子列表，调用generate_factored时，只取列表中出现的素因子
- prime_factors: 素因子数目，调用generate_factored时，生成的常数可分解为此参数指定个数的素因子数
- signed: 是否生成带符号数
# 专项练习
- unsigned_add 无符号数相加
- unsigned_sub 无符号数相减
- signed_add_sub 带符号加减
- signed_add_sub2 带符号加减（带括号，三个操作数）
- add_sub_equation 带未知数加减法
- add_sub_equation2 带未知数加减法（带括号，三个操作数）
- mul: 乘法
- div: 除法 这里应练习两种方法：1 带余除法，例如 15/7=2余1； 2 小数点除法，例如 15/7=2.143
- mul_div: 乘除混合
- mix_arithmetic: 混合四则运算
- factor: 分解素因子
- simplify: 分数化简
- gcd_and_lcm: 最大公约数和最小公倍数
- simple_rational: 有理数加减
- mul_div_equation: 乘除方程
- simple_rational_equation: 单项有理方程，考察移项规则
- rational_equation: 多项有理方程，未知数系数为单分子或单分母
- rational_equation2: 多项有理方程，考虑分离常数项和算法优先级
- rational_comparison: 带符号分数比大小
- integral_linear_equations: 整系数方程组

# 批量生成 ProblemGenerator(method, *args, count)
- method: 专项练习的函数名
- args: 专项练习传入参数
- count: 生成题目个数
