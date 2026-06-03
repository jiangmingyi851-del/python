n=int(input())
if n==0:
    print(0)
    exit()
li=list(map(int,input().split()))
pre=li[0]
num=1
current=1
for i in range(1,n):
    if li[i]==pre+1:
        current+=1
    else:
        current=1
    pre=li[i]
    num=max(num,current)
print(num)
