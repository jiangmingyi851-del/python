from collections import defaultdict
n,m=map(int,input().split())
edges=set()
li=[]
for i in range(m):
    u,v,w=map(int,input().split())
    edges.add((u,v))
    edges.add((v,u))
    li.append((w,u,v))
nxt=[i+1 for i in range(n+2)]
pre=[i-1 for i in range(n+2)]
stack=[]
comp=[0]*(n+1)
def remove(v):
    nxt[pre[v]]=nxt[v]
    pre[nxt[v]]=pre[v]
cur_comp=0
while nxt[0]!= n+1:
    cur_comp+=1
    stack.append(nxt[0])
    comp[nxt[0]]=cur_comp
    while stack:
        u=stack.pop()
        v=nxt[0]
        while v<n+1:
            if (u,v) not in edges:
                comp[v]=comp[u]
                remove(v)
                stack.append(v)
            v=nxt[v]
li.sort()
parent=[i for i in range(cur_comp+1)]
def find(x):
    if parent[x]==x:
        return x
    parent[x]=find(parent[x])
    return parent[x]
ans=0
for w,u,v in li:
    if find(comp[u])!=find(comp[v]):
        parent[find(comp[u])]=find(comp[v])
        ans+=w
print(ans)

    

        
         

