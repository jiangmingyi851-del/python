n,m=map(int,input().split())
matrix=[]
for i in range(n):
    a=list(map(int,input().split()))
    matrix.append(a)
protected=[[0]*m for i in range(n)]
def dfs_not_alone(x,y):
    for dx,dy in [[-1,0],[1,0],[0,-1],[0,1]]:
        if 0<=x+dx<n and 0<=y+dy<m and matrix[x+dx][y+dy]==1 and protected[x+dx][y+dy]==0:
            protected[x+dx][y+dy]=1
            dfs_not_alone(x+dx,y+dy)
for i in range(n):
    if matrix[i][0]==1:
        protected[i][0]=1
        dfs_not_alone(i,0)
    if matrix[i][m-1]==1:
        protected[i][m-1]=1
        dfs_not_alone(i,m-1)
for j in range(m):
    if matrix[0][j]==1:
        protected[0][j]=1
        dfs_not_alone(0,j)
    if matrix[n-1][j]==1:
        protected[n-1][j]=1
        dfs_not_alone(n-1,j)
for i in range(n):
    print(' '.join(map(str,protected[i])))


