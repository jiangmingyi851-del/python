from collections import defaultdict,deque
n,p=map(int,input().split())
bias=[0]*(n+1)
states=[0]*(n+1)
edges=defaultdict(int)
in_edges=[0]*(n+1)
out_edges=[0]*(n+1)
for i in range(n):
    states[i+1],bias[i+1]=map(int,input().split())
for i in range(p):
    a,b,u=map(int,input().split())
    edges[(a,b)]+=u
for u,v in edges.keys():
    in_edges[v]+=1
    out_edges[u]+=1
stack=deque()
not_circle=0    
ans=[]
for i in range(1,n+1):
    if in_edges[i]==0 :
        not_circle+=1
        stack.append(i)
while stack:
    node=stack.popleft()
    for i in range(1,n+1):
        if (node,i) in edges:
            in_edges[i]-=1
            if in_edges[i]==0:
                stack.append(i)
                states[i]-=bias[i]
                not_circle+=1
            if states[node]>0:
                states[i]+=edges[(node,i)]*(states[node])
    if out_edges[node]==0 and states[node]>0:
        ans.append((node,states[node]))
if not_circle!=n or len(ans)==0:
    print("NULL")
    exit()
else:
    ans.sort()
    for i in ans:
        print(i[0],i[1])







