n=int(input())
visited=[False]*100001
prime=[]
for i in range(2,100001):
    if not visited[i]:
        visited[i]=True
        prime.append(i)
        for j in range(i*i,100001,i):
            visited[j]=True
visited1=[False]*(n+1)
real=[0]*(n+1)
ans=[]
for i in range(2,n+1):
    if not visited1[i]:
        visited1[i]=True
        for j in prime:
                if i%j==0:
                    num=1
                    a=i
                    while a%j==0:
                        num+=1
                        a//=j
                    p1=(j**num-1)//(j-1)
                    real[i]=p1*(a+real[a])-i
                    if real[i]<n:
                        visited1[real[i]]=True 
                    break
    else:
        for j in prime:
                if i%j==0:
                    num=1
                    a=i
                    while a%j==0:
                        num+=1
                        a//=j
                    p1=(j**num-1)//(j-1)
                    real[i]=p1*(a+real[a])-i
                    if real[i]<n:
                        visited1[real[i]]=True 
                    break
        if  real[i]<=n and real[real[i]]<=n and real[real[i]]==i and i!=real[i]:
            ans.append((real[i],i))
ans.sort()
for i in ans:
    print(i[0],i[1])
        
                
        
        

