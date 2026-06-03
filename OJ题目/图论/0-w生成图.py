
from collections import defaultdict,deque
n,m=map(int,input().split())
parent=[(i+1)%n for i in range(n)]
child=[(i-1)%n for i in range(n)]
last_node=[i for i in range(n)]
belong=[-1]*n
ban=defaultdict(set)
w_list=[]
for i in range(m):
    a,b,w=map(int,input().split())
    ban[a-1].add(b-1)
    ban[b-1].add(a-1)
    w_list.append((w,a-1,b-1))
queue=deque()
queue.append(0)
belong[0]=1
cur_belong=1
while queue:
    u=queue.popleft()
    if belong[u]==-1:
        cur_belong+=1
        belong[u]=cur_belong
    v=u
    while parent[v]!=u:
        v=parent[v]
        if v in ban[u]:
            queue.append(v)
            continue
        else:
            last_node[v]=u
            if belong[v]==-1:
                belong[v]=belong[u]
            else:
                belong[v]=min(belong[v],belong[u])
                belong[u]=belong[v]
            a=parent[v]
            b=child[v]
            parent[b]=a
            child[a]=b
            v=u
            while last_node[v]!=v and belong[last_node[v]]>belong[v]:
                belong[last_node[v]]=belong[v]
                v=last_node[v]
    a=parent[u]
    b=child[u]
    parent[b]=a
    child[a]=b
def find(x):
    if belong[x]!=x:
        belong[x]=find(belong[x])
    return belong[x]
w_list.sort()
ans=0
for w,a,b in w_list:
    if find(a)!=find(b):
        ans+=w
        belong[find(a)]=find(b)
print(ans)





        




