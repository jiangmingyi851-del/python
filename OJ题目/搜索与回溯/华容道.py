import sys
from collections import deque
n=int(sys.stdin.readline().strip())
matrix=deque()
tar=0
for k,i in enumerate(sys.stdin.readlines()):
    for j in i.strip().split():
        if int(j)!=0:
            matrix.append(int(j))
        else:
            tar=1 if k%2==0 else 0


def merge(l1,l2):
    l=deque()
    ans=0
    while l1 and l2:
        if l1[0]<l2[0]:   
            l.append(l1.popleft())
        else:
            l.append(l2.popleft())
            ans+=len(l1)
    l.extend(l2)
    l.extend(l1)
    return l,ans
def merge_sort(l):
    if len(l)==1:
        return l,0
    mid=len(l)//2
    l1 = deque()
    for _ in range(mid):
        l1.append(l.popleft())
    l2=l.copy()
    l1,ans1=merge_sort(l1)
    l2,ans2=merge_sort(l2)
    l,ans3=merge(l1,l2)
    return l,ans1+ans2+ans3
ans=merge_sort(matrix)[1]
if n%2==0:
    if bool((ans+tar)%2==n%2):
        print('yes')
    else:
        print('no')
else:
    if not bool(ans%2==n%2):
        print('yes')
    else:
        print('no')
        
        



