n,a,b=map(int,input().split())
plants=list(map(int,input().split()))
pointer1=0
cuwater1=a
cuwater2=b
pointer2=n-1
ans=0
for i in range((n+1)//2):
    if pointer1==pointer2:
        if plants[pointer1]>max(cuwater1,cuwater2):
            ans+=1
    else:
        if plants[pointer1]<=cuwater1:
            cuwater1-=plants[pointer1]
        else:
            ans+=1
            cuwater1=a-plants[pointer1]
        if plants[pointer2]<cuwater2:
            cuwater2-=plants[pointer2]
        else:
            ans+=1
            cuwater2=b-plants[pointer2]
    pointer1+=1
    pointer2-=1
print(ans)
