class graph:
    def __init__(self,vertices ):
        self.vertices = vertices
        self.neighbours={v:[] for v in range(vertices)}

    def add_edge(self,u,v):
        self.neighbours[u].append(v)
        self.neighbours[v].append(u)
    
    def dfs(self,v,visited):
        stack=[v]
        visited[v]=True
        while stack:
            m=stack.pop()
            for i in self.neighbours[m]:
                if not visited[i]:
                    stack.append(i)
                    visited[i]=True
    
    def count_components(self):
        visited=[False]*self.vertices
        count=0
        for v in range(self.vertices):
            if not visited[v]:
                self.dfs(v,visited)
                count+=1
        return count
li=[]
while True:
    n,m=map(int,input().split())
    if n==0 and m==0:
        break
    g=graph(n)
    for _ in range(m):
        u,v=map(int,input().split())
        g.add_edge(u-1,v-1)
    li.append(g)
for a,g in enumerate(li,1):
    print(f"Case {a}: {g.count_components()}")



