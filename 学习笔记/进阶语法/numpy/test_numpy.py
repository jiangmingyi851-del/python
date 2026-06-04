import numpy as np
a = np.array([1,2,3])
print("NumPy数组:",a)

matrix = np.array([[1,2],[3,4]])
print("矩阵:\n",matrix)

print("数组形状:",a.shape)
print("矩阵形状:",matrix.shape)

# r = np.array(range(2,11,2))
r = np.array([i for i in range(2,11) if i%2 == 0])
print(r)