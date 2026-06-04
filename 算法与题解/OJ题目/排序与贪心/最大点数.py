#状态压缩
from copy import deepcopy
m,n,p=map(int,input().split())
matrix=[]
for i in range(m):
    matrix.append(list(map(int,input().split())))
for i in range(4096):
    current_matrix=deepcopy(matrix)
    li=[]
    while i>0:
        li.append(i%4)
        i//=4
    if len(li)<6:
        li.extend([0]*(6-len(li)))
    for j in li:
        if j==0:
            for i in range(m):
                for j in range(n-1):
                    if current_matrix[i][j]==current_matrix[i][j+1]:
                        current_matrix[i][j]*=2
                        current_matrix[i][j+1]=0
                for j in range(n):
                    if current_matrix[i][j]==0:
                        

    
    



