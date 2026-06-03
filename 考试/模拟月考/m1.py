from functools import lru_cache
from collections import defaultdict
n,m=map(int,input().split())
state=input()
need=[]
for i in state:
    if i=='P':
        need.append(2)
    elif i=='R':
        need.append(0)
    else:
        need.append(1)
can_accept=defaultdict(list)
can_help=defaultdict(list)
visite=[False]*m
for i in range(m):
    li=list(map(int,input().split()))
    for j in li[1:]:
        can_accept[j-1].append(i)
        can_help[i].append(j-1)
def help(numm,num,li):
    for i,j in zip(num,li):
        for k in can_help[j]:
            numm[k]=(numm[k]-i)%3
    return tuple(numm)
@lru_cache(maxsize=None)
def can_win(tup,num,visited):
    if tup==():
        return 0
    visited=list(visited)
    tupp=list(tup)
    numm=list(num)
    a=tupp.pop()
    if a not in can_accept :
        return False
    b=numm[a]
    l=0
    candi=[]
    ans=[]
    if b==0:
        for k in can_accept[a]:
            if not visited[k]:
                candi.append(k)
                visited[k]=True
                l+=1
        if l==0:
            return False
        elif l==1:
            a=can_win(tuple(tupp),help(numm,[0],candi),tuple(visited))
            if a!=False:
                return a+0
            return False
        else:
            a=can_win(tuple(tupp),help(numm,[0,0],candi),tuple(visited))
            if a!=False:
                ans.append(a+0)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[2,1],candi),tuple(visited))
            if a!=False:
                ans.append(a+3)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[1,2],candi),tuple(visited))
            if a!=False:
                ans.append(a+3)
            for k in candi:
                visited[k]=False
            if len(ans)==0:
                return False
            else:
                return min(ans)
    elif b==1:
        for k in can_accept[a]:
            if not visited[k]:
                candi.append(k)
                visited[k]=True
                l+=1
        if l==0:
            return False
        elif l==1:
             a=can_win(tuple(tupp),help(numm,[1],candi),tuple(visited))
             if a!=False:
                 return a+1
             return False
        else:
            a=can_win(tuple(tupp),help(numm,[1,0],candi),tuple(visited))
            if a!=False:
                ans.append(a+1)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[0,1],candi),tuple(visited))
            if a!=False:
                ans.append(a+1)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[2,2],candi),tuple(visited))
            if a!=False:
                ans.append(a+4)
            for k in candi:
                visited[k]=False
            if len(ans)==0:
                return False
            else:
                return min(ans)
    else:
        for k in can_accept[a]:
            if not visited[k]:
                candi.append(k)
                visited[k]=True
                l+=1
        if l==0:
            return False
        elif l==1:
            a=can_win(tuple(tupp),help(numm,[2],candi),tuple(visited))
            if a!=False:
                return a+2
            return False
        else:
            a=can_win(tuple(tupp),help(numm,[2,0],candi),tuple(visited))
            if a!=False:
                ans.append(a+2)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[0,2],candi),tuple(visited))
            if a!=False:
                ans.append(a+2)
            for k in candi:
                visited[k]=False
            a=can_win(tuple(tupp),help(numm,[1,1],candi),tuple(visited))
            if a!=False:
                ans.append(a+2)
            for k in candi:
                visited[k]=False
            if len(ans)==0:
                return False
            else:
                return min(ans)
print(can_win(tuple([i for i in range(n)]),tuple(need),tuple(visite)))

