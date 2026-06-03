from collections import deque
n=int(input())
happy=[0]*(n+1)
manager=[0]*(n+1)
employer=[[] for i in range(n+1)]
em_num=[0]*(n+1)
for i in range(1,n+1):
    happy[i]=int(input())
for i in range(n-1):
    en,ma=map(int,input().split())
    manager[en]=ma
    employer[ma].append(en)
    em_num[ma]+=1
happier=[[0,0] for i in range(n+1)]
stack=deque()
for i in range(1,n+1):
    if em_num[i]==0:
        happier[i][0]=max(happy[i],0)
        stack.append(i)
while stack:
    en=stack.popleft()
    ma=manager[en]
    em_num[ma]-=1
    if em_num[ma]==0:
        happier[ma][1]=sum(happier[en][0] for en in employer[ma])
        happier[ma][0]=max(happy[ma]+sum(happier[en][1] for en in employer[ma]),happier[ma][1])
        stack.append(ma)
for i in range(1,n+1):
    if manager[i]==0:
        print(happier[i][0])
        exit()




        
