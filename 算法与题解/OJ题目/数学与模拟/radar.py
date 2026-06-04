import math
import sys
def radar_num(n,l,d):
    l2=[]
    if n==0:
        return 0
    ans=1
    for i,j in l:
        if j>d:
            return -1
        x2=math.sqrt(d**2-j**2)+i
        x1=-math.sqrt(d*d-j*j)+i
        l2.append((x1,x2))
    l2.sort()
    edge=l2[0][1]
    for i in range(n):
        if l2[i][0]>edge:
            ans+=1
            edge=l2[i][1]
        else:
            edge=min(edge,l2[i][1])
    return ans
k=0
while True:
    l=[]
    n,d=map(int,sys.stdin.readline().strip().split())
    if n==0 and d==0:
        break
    k+=1
    for i in range(n):
        x,y=map(int,sys.stdin.readline().strip().split())
        l.append((x,y))
    b=input()
    print(f'Case {k}: {radar_num(n,l,d)}')
   
