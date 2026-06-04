n,m=map(int,input().split())
neighbor=[[] for i in range(n)]
edges=[0]*n
for i in range(m):
    a,b=map(int,input().split())
    neighbor[a].append(b)
    edges[b]=edges[b]+1
stack=[]
for i in range(n):
    if edges[i]==0:
        stack.append(i)
while stack:
    node=stack.pop()
    for i in neighbor[node]:
        edges[i]=edges[i]-1
        if edges[i]==0:
            stack.append(i)
if sum(edges)==0:
    print("No")
else:
    print("Yes")


