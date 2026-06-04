# import heapq
# from collections import defaultdict
# m,n,p=map(int,input().split())
# maze=[input().split() for i in range(m)]
# visited=[[False]*n for i in range(m)]
# distance=[[float('inf')]*n*m  for i in range(m*n)]
# for i in range(m):
#     for j in range(n):
#         distance[i*n+j][i*n+j]=0
#         if maze[i][j].isdigit():
#             for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
#                 x,y=i+dx,j+dy
#                 if 0<=x<m and 0<=y<n and maze[x][y]!='#':
#                     distance[i*n+j][x*n+y]=abs(int(maze[i][j])-int(maze[x][y]))
#                     distance[x*n+y][i*n+j]=abs(int(maze[i][j])-int(maze[x][y]))
# for k in range(m*n):
#     for i in range(m*n):
#         for j in range(m*n):
#             if distance[i][k]!=float('inf') and distance[k][j]!=float('inf') and distance[i][j]>distance[i][k]+distance[k][j]:
#                 distance[i][j]=distance[i][k]+distance[k][j]
# for i in range(p):
#     x1,y1,x2,y2=map(int,input().split())
#     if distance[x1*n+y1][x2*n+y2]==float('inf'):
#         print('NO')
#     else:
#         print(distance[x1*n+y1][x2*n+y2])
import heapq
from collections import defaultdict
m,n,p=map(int,input().split())
maze=[input().split() for i in range(m)]
visited=set()
def dijkstra(start,end):
    if start==end:
        return 0
    heap=[]
    heapq.heappush(heap,(0,start))
    distance=[[float('inf')]*n  for i in range(m)]
    while heap:
        dist,node=heapq.heappop(heap)
        if dist>distance[node//n][node%n] or maze[node//n][node%n]=='#':
            continue
        x,y=node//n,node%n
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<m and 0<=ny<n and maze[nx][ny]!='#':
                new_dist=dist+abs(int(maze[x][y])-int(maze[nx][ny]))
                if new_dist<distance[nx][ny]:
                    distance[nx][ny]=new_dist
                    heapq.heappush(heap,(new_dist,nx*n+ny))
    return distance[end//n][end%n]
for i in range(p):
    x1,y1,x2,y2=map(int,input().split())
    dist=dijkstra(x1*n+y1,x2*n+y2)
    if dist==float('inf'):
        print('NO')
    else:
        print(dist)






    
            
        


