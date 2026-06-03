import heapq
a,b,c=map(int,input().split())
q=int(input())
max_factor=1
if a==0 and b==0 and c==0:
    for i in range(q):
        u=int(input())
        print('No')
    exit()
if a==0 and c!=0:
    for j in range(c,1,-1):
        if  a%j==0 and b%j==0 and c%j==0:
            max_factor=j
            break
elif b!=0:
    for j in range(b,1,-1):
        if  a%j==0 and b%j==0 and c%j==0:
            max_factor=j
            break
else:
    for j in range(a,1,-1):
        if  a%j==0 and b%j==0 and c%j==0:
            max_factor=j
            break
a//=max_factor
b//=max_factor
c//=max_factor
dist=[-1]*(max(a,b,c))
dist[0]=0
r=len(dist)
def dijkstra(l):
    if (l%max_factor)!=0:
        return -1
    if dist[(l//max_factor)%r]!=-1:
        return dist[(l//max_factor)%r]

    queue=[]
    end=(l//max_factor)%r
    heapq.heappush(queue,(0,0))
    while queue:
        cur,num=heapq.heappop(queue)
        if cur>dist[num]:
            continue
        for j in (a,b,c):
            if j==0:
                continue
            next_num=(num+j)%r
            cur_plus=(num+j)//r
            if dist[next_num]==-1 or dist[next_num]>cur_plus+cur:
                dist[next_num]=cur_plus+cur
                heapq.heappush(queue,(cur_plus+cur,next_num))
    return dist[end]
for i in range(q):
    v=int(input())
    numb=v//(max_factor*r)
    d=dijkstra(v)
    if d==-1:
        print('No')
    else:
        if numb<d:
            print('No')
        else:
            print('Yes')

    