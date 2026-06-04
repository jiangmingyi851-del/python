n,m=map(int,input().split())
l1=[]
l2=[]
l=[]
for i in range(n):
    x,y=map(int,input().split())
    l1.append(x)
    l2.append(y)
    l.append(x+y)
l.sort()
l1.sort()
l2.sort()
sum1=0
usag=0
for i in l1:
    if i<=l[0]//2:
        sum1+=1
        usag+=i
a=((m-usag)//(l[0]))*2+sum1
if ((m-usag)//l[0]+1)*l[0]>=m:
    print(a)
    exit()
else:
    num1=((m-usag)//l[0]+1)*2
    b1=(num1//2)*l[0]
    b2=m-b1
    for i in l1:
        if i<=b2:
            num1+=1
            b2-=i
    print(max(num1,a))



