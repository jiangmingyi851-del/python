import sys
def vaid_number(grid,k):
    ans=0
    if not grid:
        return 0
    if k>len(grid) or k>len(grid[0]):
        return 0
    if k==0:
        return 1
    if len(grid)==1:
        return grid[0].count(1) 
    if len(grid[0])==1:
        return sum(row[0] for row in grid)
    for j,i in enumerate(grid[0]):
        if i==1:
            ans+=vaid_number([row[:j]+row[j+1:] for row in grid[1:]],k-1)
    ans+=vaid_number([row for row in grid[1:]],k)
    return ans
li=[]
while True:
    n,k=map(int,sys.stdin.readline().strip().split())
    if n==-1 and k==-1:
        break
    grid=[[0]*n for _ in range(n)]
    for _ in range(n):
        a=list(str(sys.stdin.readline().strip()))
        if len(a)!=n:
            break
        for j,i in enumerate(a):
            if i=='#':
                grid[_][j]=1
    li.append((grid,k))
for grid,k in li:
    print(vaid_number(grid,k))
        
    


        
