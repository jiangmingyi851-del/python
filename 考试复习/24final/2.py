from collections import deque
n,m=map(int,input().split())
children=list(map(int,input().split()))
candyneed=deque([(children[i],i) for i in range(n)])
while len(candyneed)>1:
    childneed,childindex=candyneed.popleft()
    if childneed>m:
        candyneed.append((childneed-m,childindex))
print(candyneed[0][1]+1)
