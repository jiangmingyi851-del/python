n,m=map(int,input().split())
points=[]
matrix=[]
for i in range(n):
    li=list(map(int,input().split()))
    for k,j in enumerate(li):
        if j==1:
            points.append(i*n+k)
    matrix.append(li)
parents={s:s for s in points }
def find(x):
    if parents[x]!=x:
        parents[x]=find(parents[x])
    return parents[x]
def union(a,b):
    a=find(a)
    b=find(b)
    if a!=b:
        parents[b]=a
for i in points:
    x,y =i//n,i%n
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx,ny=x+dx,y+dy
        if 0<=nx<n and 0<=ny<m and matrix[nx][ny]==1:
            union(i,nx*n+ny)
ans=set()
for i in points:
    if find(i) not in ans:
        ans.add(find(i))
print(len(ans))