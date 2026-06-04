def op_num(k):
    return k*(k-1)//2
n,q=map(int,input().split())
parent=[i for i in range(n+1)]
size=[1]*(n+1)
rank=[0]*(n+1)
def find(x):
    if parent[x]!=x:
        parent[x]=find(parent[x])
    return parent[x]
ans=0
def union(a,b):
    global ans
    u,v=find(a),find(b)
    if u==v:
        return
    if rank[u]>rank[v]:
        parent[v]=u
    elif rank[u]<rank[v]:
        parent[u]=v
    else:
        parent[v]=u
        rank[u]+=1
    ans+=op_num(size[u]+size[v])-op_num(size[u])-op_num(size[v])
    size[u]+=size[v]
    size[v]=size[u]
for i in range(q):
    a,b=map(int,input().split())
    union(a,b)
    print(ans)




    