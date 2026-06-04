li=list(map(int,input().split()))
state=0
pre=li[0]
ans=1
curr=1
for i in range(1,len(li)):
    if li[i]>pre:
        if state==0 or state==1:
            state=1
            curr+=1
        else:
            ans=max(ans,curr)
            curr=2
            state=1
    elif li[i]==pre:
        if state==-1:
           ans=max(ans,curr)
        curr=1
        state=0
    else:
        if state==-1 or state==1:
            state=-1
            curr+=1
            ans=max(ans,curr)
        else:
            state=0
            curr=1
    pre=li[i]
if ans<=2:
    print(0)
else:
    print(ans)
            