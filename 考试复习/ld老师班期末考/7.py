n=int(input())
for i in range(n):
    li=list(map(int,input().split()))
    if sum(li)==n-1:
        print(i)
    else:
        continue
