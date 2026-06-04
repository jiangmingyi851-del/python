n=int(input())
from functools import lru_cache
import sys
sys.setrecursionlimit(1000000)
for j in range(n):
    t=int(input())
    neighbours=[[] for i in range(t+1)]
    children=[[] for i in range(t+1)]
    parent=[0]*(t+1)
    for i in range(t-1):
        a,b=map(int,input().split())
        neighbours[b].append(a)
        neighbours[a].append(b)
    stack=[1]
    li=[]
    while stack:
        node=stack.pop()
        li.append(node)
        for neighbour in neighbours[node]:
            if neighbour!=parent[node]:
                parent[neighbour]=node
                children[node].append(neighbour)
                stack.append(neighbour)
    leaf_cnt=[0]*(t+1)
    for i in range(t-1,-1,-1):
        node=li[i]
        if not children[node]:
            leaf_cnt[node]=1
        else:
            for child in children[node]:
                leaf_cnt[node]+=leaf_cnt[child]
    q=int(input())
    for i in range(q):
        x,y=map(int,input().split())
        ans=leaf_cnt[x]*leaf_cnt[y]
        print(ans)

