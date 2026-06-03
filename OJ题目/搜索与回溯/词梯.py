from collections import defaultdict,deque
n=int(input())
neighbor=defaultdict(list)
dic=defaultdict(list)
for j in range(n):
    s=input()
    s1='x'+s[1:]
    for i in dic[s1]:
        neighbor[i].append(s)
        neighbor[s].append(i)
    dic[s1].append(s)
    s2=s[:1]+'x'+s[2:]
    for i in dic[s2]:
        neighbor[i].append(s)
        neighbor[s].append(i)
    dic[s2].append(s)
    s3=s[:2]+'x'+s[3:]
    for i in dic[s3]:
        neighbor[i].append(s)
        neighbor[s].append(i)
    dic[s3].append(s)
    s4=s[:3]+'x'
    for i in dic[s4]:
        neighbor[i].append(s)
        neighbor[s].append(i)
    dic[s4].append(s)
start,end=input().split()
visited=set()
stack=deque([start])
last={}
if start==end:
    print(start)
    exit()
while stack:
    node=stack.popleft()
    for i in neighbor[node]:
        if i not in visited:
            visited.add(i)
            stack.append(i)
            last[i]=node
            if i==end:
                stack.clear()
                break
if end not in last:
    print('NO')
else:
    res=[end]
    while res[-1]!=start:
        res.append(last[res[-1]])
    print(' '.join(res[::-1]))



