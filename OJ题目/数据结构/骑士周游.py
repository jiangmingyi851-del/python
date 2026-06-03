n=int(input())
u,v=map(int,input().split())
neighbour=[[0]*n for j in range(n)]
for i in range(n):
    for j in range(n):
        for dx, dy in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                if 0<=i+dx<n and 0<=j+dy<n:
                    neighbour[i][j]+=1
neighbour_nums=[[[] for i in range(n)] for j in range(n)]
for i in range(n):
    for j in range(n):
         for dx, dy in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                if 0<=i+dx<n and 0<=j+dy<n:
                    neighbour_nums[i][j].append((neighbour[i+dx][j+dy],i+dx,j+dy))

visited=[[False]*n for j in range(n)]
def dfs(x,y,node_num):
    visited[x][y]=True
    if node_num==n**2:
        return True
    for n_num,n_x,n_y in sorted(neighbour_nums[x][y]):
        if not visited[n_x][n_y]:
            if dfs(n_x,n_y,node_num+1):
                return True
    visited[x][y]=False
    return False
print("success" if dfs(u,v,1) else "fail")
    
         
    