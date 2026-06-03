import matplotlib.pyplot as plt
import numpy as np

# 基础变换矩阵定义
rot_cw90 = np.array([[0, 1], [-1, 0]])    # 顺时针90度旋转
rot_ccw90 = np.array([[0, -1], [1, 0]])  # 逆时针90度旋转
reflect_x = np.array([[1, 0], [0, -1]])  # x轴对称反射
reflect_y = np.array([[-1, 0], [0, 1]])  # y轴对称反射

# 示例标准正交基（单位正交向量组）
bases = [
    # (e1, e2, 标签, 变换操作)
    (np.array([0.6,0.8]), np.array([-0.8,0.6]), "1、一→二象限基", rot_cw90),
    (np.array([-0.7,0.7]), np.array([-0.7,-0.7]), "2、二→三象限基", reflect_x),
    (np.array([-0.6,-0.8]), np.array([0.8,-0.6]), "3、三→四象限基", rot_cw90),
    (np.array([0.7,-0.7]), np.array([0.7,0.7]), "4、四→一象限基", reflect_x),
]

# 创建画布
plt.figure(figsize=(8,8), dpi=110)
plt.axhline(0, c='k', lw=1, alpha=0.6)
plt.axvline(0, c='k', lw=1, alpha=0.6)
plt.grid(alpha=0.3)
plt.xlim(-1.6,1.6)
plt.ylim(-1.6,1.6)

# 绘制每一组原基+变换后基
for e1, e2, name, trans in bases:
    # 画原始标准正交基（蓝色）
    plt.quiver(0,0, e1[0],e1[1], angles='xy',scale_units='xy',scale=1, color='#2980b9', width=0.012, label='原基' if name==bases[0][2] else "")
    plt.quiver(0,0, e2[0],e2[1], angles='xy',scale_units='xy',scale=1, color='#3498db', width=0.012)
    
    # 计算并画变换后的基（红色）
    e1_t = trans @ e1
    e2_t = trans @ e2
    plt.quiver(0,0, e1_t[0],e1_t[1], angles='xy',scale_units='xy',scale=1, color='#c0392b', width=0.012, label='映射后基' if name==bases[0][2] else "")
    plt.quiver(0,0, e2_t[0],e2_t[1], angles='xy',scale_units='xy',scale=1, color='#e74c3c', width=0.012)

# 标注象限
plt.text(1.2,1.2,"第一象限",fontsize=10)
plt.text(-1.4,1.2,"第二象限",fontsize=10)
plt.text(-1.4,-1.4,"第三象限",fontsize=10)
plt.text(1.2,-1.4,"第四象限",fontsize=10)

plt.title("σ非满射的二维反例：分段混合正交变换", fontsize=13, pad=15)
plt.legend(loc='upper right')
plt.show()