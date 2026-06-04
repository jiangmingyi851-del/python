import heapq
import sys
while True:
    try:
        line = sys.stdin.readline()
        if not line:
            break
        n = int(line.strip())
    except EOFError:
        break
    distance=[list(map(int,sys.stdin.readline().strip().split())) for i in range(n)]
    ans=0
    visited=set([0])
    edges=[(cost,0,to) for to,cost in enumerate(distance[0]) if to!=0]
    heapq.heapify(edges)
    while edges:
        cost,from_,to=heapq.heappop(edges)
        if to in visited:
            continue
        ans+=cost
        visited.add(to)
        for to_,cost_ in enumerate(distance[to]) :
            if to_ not in visited :
                heapq.heappush(edges,(cost_,to,to_))
    print(ans)

