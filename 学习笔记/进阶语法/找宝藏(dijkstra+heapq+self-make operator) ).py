import heapq
class iteam:
    def __init__(self,x,y,len):
        self.x=x
        self.y=y
        self.len=len
    def __lt__(self,other):
        return self.len<other.len
        
def find_1(Map,m,n):
    if Map[0][0]==1:
        return 0
    move=[(1,0),(-1,0),(0,1),(0,-1)]
    visited=[[False]*n for _ in range(m)]
    x,y=0,0
    visited[0][0]=True 
    q=[iteam(0,0,0)] 
    while q:
        a=heapq.heappop(q)
        x=a.x
        y=a.y
        leng=a.len
        for dx,dy in move:
            x1=x+dx
            y1=y+dy
            if 0<=x1<=m-1 and 0<=y1<=n-1:
                if Map[x1][y1]==0 and visited[x1][y1]==False:
                    heapq.heappush(q,iteam(x1,y1,leng+1))
                    visited[x1][y1]=True
                if Map[x1][y1]==1:
                    return leng+1
    return "NO"
m,n=map(int,input().strip().split())
Map=[]
for i in range(m):
    li=list(map(int,input().strip().split()))
    Map.append(li)
print(find_1(Map,m,n))


            



