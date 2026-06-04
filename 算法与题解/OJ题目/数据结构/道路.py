import heapq
k = int(input())
n=int(input())
r=int(input())
graph=[[] for i in range(n+1)]
for i in range(r):
    s,d,l,t = map(int,input().split()) # Read the edge information
    graph[s].append((d,l,t)) # Add the edge to the graph
dist=[float('inf') for i in range(n+1)]
costs=[float('inf') for i in range(n+1)]
dist[1]=0
costs[1]=0
def dijkstra():
    pq = [(0,0,1)] # Initialize the priority queue with the starting point
    while pq:
        d,cost,u = heapq.heappop(pq)
        costs[u]=min(costs[u],cost) # Get the edge with the smallest distance
        for v,l,t in graph[u]: # Iterate over the edges connected to the current node
            if ( d+l< dist[v] and cost + t <=k)or (cost+t<=k and cost+t<costs[v]): 
                if d + l < dist[v]: # If the new distance is smaller, update it
                    dist[v] = d + l 
                heapq.heappush(pq,(d+l,cost+t,v)) 
dijkstra()
if dist[n]==float('inf'):
    print(-1)
else:
    print(dist[n])
 

