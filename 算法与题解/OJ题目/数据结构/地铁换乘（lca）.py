#这题其实不算是lca,先写一个随便能过的
n,t=map(int,input().split())
neighbor=[[] for _ in range(n+1)]
for _ in range(n-1):
    u,v=map(int,input().split())
    neighbor[u].append(v)
    neighbor[v].append(u)
parents=[-1]*(n+1)
children=[[] for _ in range(n+1)]
depth=[0]*(n+1)
def dfs(node,parent):
    parents[node] = parent
    for neighbor_node in neighbor[node]:
        if neighbor_node != parent:
            depth[neighbor_node]=depth[node]+1
            children[node].append(neighbor_node)
            dfs(neighbor_node, node)
dfs(t,-1)
p,q,v1,v2=map(int,input().split())
def get_path(node1,node2):
    path1_to_ancestor=[]
    path2_to_ancestor=[]
    while depth[node2]>depth[node1]:
        path2_to_ancestor.append(node2)
        node2=parents[node2]
    while depth[node1]>depth[node2]:
        path1_to_ancestor.append(node1)
        node1=parents[node1]
    while node1!=node2:
        path1_to_ancestor.append(node1)
        path2_to_ancestor.append(node2)
        node1=parents[node1]
        node2=parents[node2]
    path=path1_to_ancestor+[node1]+path2_to_ancestor[::-1]
    return path
path=get_path(p,q)
days=(len(path)-1)//(v1+v2)
station=path[days*v1]
print(days,depth[station])

#现在假设他要修很多条，这个时候就要用lca了。
r=n.bit_length()
up=[[0]*(r) for _ in range(n+1)]
up[t][0]=1
stack=[t]
while stack:
    node=stack.pop()
    for i in range(1,r):
        up[node][i]=up[up[node][i-1]][i-1]
    for child in children[node]:
        up[child][0]=node
        stack.append(child)
def lca(node1,node2):
    if depth[node1]<depth[node2]:
        node1,node2=node2,node1
    for i in range(r-1,-1,-1):
        if depth[up[node1][i]]>=depth[node2]:
            node1=up[node1][i]
    if node1==node2:
        return node1
    for i in range(r-1,-1,-1):
        if up[node1][i]!=up[node2][i]:
            node1=up[node1][i]
            node2=up[node2][i]
    return up[node1][0]
anc=lca(p,q)
long1=depth[p]-depth[anc]
long2=depth[q]-depth[anc]
days=(long1+long2)//(v1+v2)
if long1>=days*v1:
    r=days*v1
    station=p
    while r>0:
        k=r&(-r)
        station=up[station][k.bit_length()-1]
        r-=k
print(days,depth[station])
