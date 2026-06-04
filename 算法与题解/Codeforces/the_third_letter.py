import sys
sys.setrecursionlimit(100000000)
data=sys.stdin.read().strip().split()
t=int(data[0])
idx=1
for i in range(t):
    n,m=int(data[idx]),int(data[idx+1])
    idx+=2
    graph=[[] for _ in range(n+1)]
    for j in range(m):
        a,b,d=int(data[idx]),int(data[idx+1]),int(data[idx+2])
        idx+=3
        graph[a].append((b,d))
        graph[b].append((a,-d))
    visited=[False]*(n+1)
    def dfs(node):
        visited[node]=True
        for neighbor,distance in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)
    start_queue=[]
    for i in range(1,n+1):
        if not visited[i]:
            start_queue.append(i)
            dfs(i)
    position=[float('inf')]*(n+1)
    can=1
    for i in start_queue:
        position[i]=0
        stack=[i]
        while stack:
            cur=stack.pop()
            for neighbor,distance in graph[cur]:
                if position[neighbor]==float('inf'):
                    position[neighbor]=position[cur]+distance
                    stack.append(neighbor)
                else:
                    if position[neighbor]!=position[cur]+distance:
                        can=0
                        break
    if not can:
        print('NO')
    else:
        print('YES')
    

        
    
