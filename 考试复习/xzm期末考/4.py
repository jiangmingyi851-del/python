
from collections import deque
sta,one,two=map(int,input().split())
nei=[[] for i in range(sta)]
for i in range(sta):
    li=list(map(int,input().split()))
    for j in range(sta):
        if i!=j and li[j]==1:
            nei[i].append(j)
if one==two:
    print(0)
    exit()
q1=deque()
q2=deque()
q1.append((one))
q2.append(two)
# vis1=[False]*sta
# vis2=[False]*sta
# vis1[one]=True
# vis2[two]=True
dic1={}
dic2={}
dic1[one]=0
dic2[two]=0
while q1 or q2:
    if q1:
        a=q1.popleft()
        for i in nei[a]:
            if i not in dic1:
                dic1[i]=dic1[a]+1
                q1.append(i)
        if i in dic2:
            if dic2[i]==dic1[i]:
                print(dic1[i])
                exit()
    if q2:
        b=q2.popleft()
        for i in nei[b]:
            if i not in dic2:
                dic2[i]=dic2[b]+1
                q2.append(i)
        if i in dic1:

            if dic1[i]==dic2[i]:
                print(dic2[i])  
                exit()
print(-1)
    

