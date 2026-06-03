import heapq
import sys
import array
n,m=map(int,input().split())
path = [array.array('i', map(int, sys.stdin.readline().split())) for _ in range(n)]
if n==1 and m==1:
    print(0)
    exit()
start=path[0][0]
end=path[n-1][m-1]
visited = bytearray(n * m)
min_cost=[10**9]*(n*m)
q=[]
heapq.heappush(q,(0,0,0))
while q:
    cost,i,j=heapq.heappop(q)
    visited[i*m+j]=1
    if i==n-1 and j==m-1:
        print(cost)
        exit()
    for x,y in [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]:
        if 0<=x<n and 0<=y<m and not visited[x*m+y]:
            new_cost=max(cost,abs(path[x][y]-path[i][j]))
            if new_cost<min_cost[x*m+y]:
                min_cost[x*m+y]=new_cost
                heapq.heappush(q,(new_cost,x,y))
    

