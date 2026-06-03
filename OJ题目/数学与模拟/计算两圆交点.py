from sympy import symbols, Eq, solve
from sympy.geometry import Point, Circle
import math
def calculate_circle_intersections(x1, y1, r1, x2, y2, r2):
    # 定义符号变量
    x, y = symbols('x y')
    
    # 定义两个圆的方程
    circle1 = Eq((x - x1)**2 + (y - y1)**2, r1**2)
    circle2 = Eq((x - x2)**2 + (y - y2)**2, r2**2)
    
    # 求解方程组
    solutions = solve((circle1, circle2), (x, y))
    
    return solutions
# 示例使用
x1, y1, r1 = 0, 0, 5  # 第一个圆的圆心和半径
x2, y2, r2 = 4, 0, 5  # 第二个圆的圆心和半径    
intersections = calculate_circle_intersections(x1, y1, r1, x2, y2, r2)
if intersections:
    for point in intersections:
        print(f"Intersection Point: ({point[0]:.2f}, {point[1]:.2f})")   

