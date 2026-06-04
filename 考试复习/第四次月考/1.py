import heapq
k=int(input())
for i in range(k):
    n=int(input())
    ma=[]
    for i in range(n):
        li=input()
        ma.append(li)
    x1,y1,x2,y2=map(int,input().split())
    visited=[[False]*n for i in range(n)]
    start=(abs(x1-x2)+abs(y1-y2),x1,y1)
    visited[x1][y1]=True
    if ma[x2][y2]=='#' or ma[x1][y1]=='#':
        print('NO')
        continue
    elif x1==x2 and y1==y2:
        print('YES')
        continue
    queue=[start]
    while queue:
        cur=heapq.heappop(queue)
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=cur[1]+dx,cur[2]+dy
            if 0<=nx<n and 0<=ny<n and not visited[nx][ny] and ma[nx][ny]=='.':
                visited[nx][ny]=True
                if (nx,ny)==(x2,y2):
                    print('YES')
                    break
                else:
                    heapq.heappush(queue,(abs(nx-x2)+abs(ny-y2),nx,ny))
    if not visited[x2][y2]:
        print('NO')

                


