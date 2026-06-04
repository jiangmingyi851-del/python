import heapq
while True:
    n=int(input())
    if n==0:
        break
    minutes=12*int(input())
    initial_catches=list(map(int,input().split()))
    decreasing_catches=list(map(int,input().split()))
    distances=list(map(int,input().split()))
    if minutes==0:
        print(', '.join(map(str,[0]*n)))
        print(f'Number of fish expected: 0')
        print()
        continue
    fishs=0
    k=0
    ans=[]
    for l in range(n):
        li=[0]*n
        fishes=0
        dis=sum(distances[:l]) if l!=0 else 0
        if dis>=minutes:
            break
        left=minutes-dis
        catches=[(-initial_catches[j],j) for j in range(l+1)]
        heapq.heapify(catches)
        for i in range(left):
            d,j=heapq.heappop(catches)
            fishes+=-d
            li[j]+=5
            d=d+decreasing_catches[j] 
            if d>0:
                d=0
            heapq.heappush(catches,(d,j))
        ans.append(li)
        if fishes>fishs:
            fishs=fishes
            k=l
    print(', '.join(map(str,ans[k])))
    print(f'Number of fish expected: {fishs}')
    print()
        
    
        





        
