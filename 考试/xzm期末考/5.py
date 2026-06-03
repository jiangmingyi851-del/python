a,b,c,d,e=map(int,input().split())
sum=0
sum+=a
if d>a*5:
    d-=a*5
    if e>a:
        e-=a
    else:
        e=0
else:
    e=max(0,e-a*11+d*2)
    d=0
if b%2==1:
    k=(b+1)//2
    sum+=(b+1)//2
    c1=c
    c=max(0,c-b-3)
    d1=d
    d=max(0,d-(36*k-b*3*4-(c1-c)*3*2)//2)
    e=max(0,e-(36*k-b*3*4-(c1-c)*3*2-(d1-d)*2))
else:
    k=b//2
    sum+=b//2
    c1=c
    c=max(0,c-b)
    d1=d
    d=max(0,d-(36*k-b*3*4-(c1-c)*3*2)//2)
    e=max(0,e-(36*k-b*3*4-(c1-c)*3*2-(d1-d)*2))
sum+=(c+5)//6
k1=(c+5)//6
c1=c
sum+=max(0,((d*2+e+35-k1*36+c*6)//36))
print(sum)




