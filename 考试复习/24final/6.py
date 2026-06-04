n=int(input())
adj=[[] for i in range(26)]
for i in range(n):
    s=input()
    a=s[0]
    b=s[-1]
    if s[1:-1]=='==':
        adj[ord(a)-ord('a')].append((ord(b)-ord('a'),0))
        adj[ord(b)-ord('a')].append((ord(a)-ord('a'),0))
    else:
        adj[ord(a)-ord('a')].append((ord(b)-ord('a'),1))
        adj[ord(b)-ord('a')].append((ord(a)-ord('a'),1))
color=[-1]*26
def dfs(i):
    cur=color[i]
    for j in adj[i]:
        if color[j[0]]==-1:
            if j[1]==0:
                color[j[0]]=cur
            else:
                color[j[0]]=1-cur
            dfs(j[0])
        elif color[j[0]]==cur:
            if j[1]==1:
                return False
        else:
            if j[1]==0:
                return False
    return True

for i in range(26):
    if color[i]==-1:
        color[i]=0
        if not dfs(i):
            print('False')
            exit()
        else:
            print('True')
            exit()