x,n=map(int,input().split())
li=list(map(int,input().split()))
li.sort()
if x==0:
    print(0)
elif  n==0 or li[0]>1:
    print(-1)
elif n==1 and li[0]==1:
    print(x)
else:
    current=1
    index=1
    num=1
    while current<x:
        if li[index]<=current+1 and index!=n-1:
            index+=1 
        elif li[index]>current+1:
                current+=li[index-1]
                num+=1
        else:
            current+=li[index]
            num+=1
    print(num)
        

