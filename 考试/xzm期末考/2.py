def two(n):
    num=''
    while n>0:
        k=n%2
        num=str(k)+num
        n//=2
    return num
li=[]
prim={}
visited=[False]*65534
for i in range(2,65534):
    if not visited[i]:
        prim[two(i)]=i
        if two(i)[::-1] in prim:
            li.append((prim[two(i)],prim[two(i)[::-1]]))
    for j in range(i*i,65534,i):
            visited[j]=True
li.sort()
n=int(input())
print(li[n-1][0]*li[n-1][1])

left=0
right=1000
mid=500
while left<right:
    a=query(mid)
    if a==1:
        right=mid
    elif a==-1:
        left=mid+1
    else:
        break
    mid=(left+right)//2