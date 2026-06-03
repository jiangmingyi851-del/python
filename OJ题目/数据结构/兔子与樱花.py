from collections import deque
import heapq
p=int(input())
id=0
name_to_id={}
id_to_name={}
for i in range(p):
    l=input().strip()
    if l not in name_to_id:
        name_to_id[l]=id
        id_to_name[id]=l
        id+=1

q=int(input())
direct_dis={}
neighbour=[[]for i in range(p)]
for i in range(q):
    l1,l2,dis=input().split()
    direct_dis[(name_to_id[l1],name_to_id[l2])]=int(dis)
    direct_dis[(name_to_id[l2],name_to_id[l1])]=int(dis)
    neighbour[name_to_id[l1]].append(name_to_id[l2])
    neighbour[name_to_id[l2]].append(name_to_id[l1])

def dijkstra(start,distance,end,path):
    if start==end:
        return 0
    stack=[]
    heapq.heappush(stack,(0,start,-1))
    while stack:
        dis,top,last=heapq.heappop(stack)
        if dis>distance[top]:
            continue
        path[top]=last
        if top==end:
            return path
        for i in neighbour[top]:
            if distance[i]>distance[top]+direct_dis[(top,i)]:
                distance[i]=distance[top]+direct_dis[(top,i)]
                heapq.heappush(stack,(distance[i],i,top))
    return -1
r=int(input())
for i in range(r):
    l1,l2=input().split()
    start=name_to_id[l1]
    end=name_to_id[l2]
    distance=[float('inf')]*p
    distance[start]=0
    path=[-1]*p
    ans=dijkstra(start,distance,end,path)
    if ans==-1:
        print("No route found")
    else:
        route=[]
        k=end
        route.append(k)
        while k!=start:
            k=path[k]
            route.append(k)
        route.reverse()
        if len(route)==1:
            print(f'{id_to_name[route[0]]} ')
        else:
            for i in range(len(route)-1):
                print(f'{id_to_name[route[i]]}->({direct_dis[(route[i],route[i+1])]})->'
            ,end='')
            print(id_to_name[route[-1]])
            

    


