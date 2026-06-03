import sys
from collections import defaultdict
sys.setrecursionlimit(1<<30)
data=sys.stdin.readlines()
n,m=map(int,data[0].split())
attitud=list(data[2])
attitude=[0]*(n+1)
for i in range(n):
    if attitud[i]=='R':
        attitude[i]=0
    elif attitud[i]=='P':
        attitude[i]=1
    else:
        attitude[i]=2
volunteers=[]
students=[[] for i in range(n+1)]
for i in range(3,3+m):
    li=list(map(int,data[i].split()))
    num=li[0]
    volunteers.append(li[1:])
    for j in li[1:]:
        students[j].append(i-3)
visited=[0]*(n+1)
comp=[0]*(n+1)
comp_first=defaultdict(int)
def dfs(stu,com):
    if visited[stu]:
        return
    visited[stu]=1
    comp[stu]=com
    if comp_first[com]==0 or len(students[comp_first[com]])>len(students[stu]):
        comp_first[com]=stu
    for v in students[stu]:
        for j in volunteers[v]:
            if not visited[j]:
                dfs(j,com)
compidx=0
for i in range(1,n+1):
    if not visited[i]:
        comidx+=1
        dfs(i,comidx)
ans=[-1]*(m)
def dfs2(stu,used,plus,ans):
    cur=attitude[stu]+plus
    can=[]
    for v in students[stu]:
        if not used[v]:
            can.append(v)
    if len(can)==0 and cur%3!=0:
        return False
    if len(can)==1:
        v=can[0]
        state=(3-cur%3)%3
        used[v]=1
        ans[v]=state
        for j in can[0]:
            if j!=stu :
                ansplus=dfs2(j,used,state,ans)
                if not ansplus:
                    return False
        used[v]=0
        return ans
    if len(can)>1:
        v=can[0]
        state=(3-cur%3)%3
        for i in range(3):
            state+=i
            used[v]=1
            an=dfs2(v,used,state,ans[:])
            




    






