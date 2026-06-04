from collections import defaultdict
n=int(input()) 
graph1=[[] for i in range(n+1)]
graph2=[[] for i in range(n+1)]
for i in range(n):
    li=list(map(int,input().split()))
    li.pop()
    for j in li:
        graph1[i+1].append(j)
        graph2[j].append(i+1)

visited=[False]*(n+1)
stack=[]
def dfs1(node):
    visited[node]=True
    for neighbor in graph1[node]:
        if not visited[neighbor]:
            dfs1(neighbor)
    stack.append(node)
for i in range(1,n+1):
    if not visited[i]:
        dfs1(i)
visited=[False]*(n+1)
comp=[]
co=defaultdict(int)
def dfs2(node,com,idx):
    visited[node]=True
    com.append(node)
    co[node]=idx
    for neighbor in graph2[node]:
        if not visited[neighbor]:
            dfs2(neighbor,com,idx)
idx=0
while stack:
    node=stack.pop()
    if not visited[node]:
        com=[]
        idx+=1
        dfs2(node,com,idx)
        comp.append(com)
ans1=0
ans2=0
if len(comp)==1:
    print(1)
    print(0)
    exit()
else:
    matrix=[[] for i in range(len(comp)+1)]
    in_degree=[0]*(len(comp)+1)
    out_degree=[0]*(len(comp)+1)
    for i in range(1,n+1):
        for neighbor in graph1[i]:
            if co[i]!=co[neighbor] and co[neighbor] not in matrix[co[i]]:
                matrix[co[i]].append(co[neighbor])
                in_degree[co[neighbor]]+=1
                out_degree[co[i]]+=1
    for i in range(1,len(comp)+1):
        if out_degree[i]==0:
            ans1+=1
        if in_degree[i]==0:
            ans2+=1
    print(ans2)
    print(max(ans1,ans2))

