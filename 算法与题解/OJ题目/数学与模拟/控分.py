t=int(input())
for i in range(t):
    r,x,d,n=map(int,input().split())
    rounds=input()
    nums=0
    for i in rounds:
        if r<x:
            nums+=1
        else:
            if i=='1':
                r=max(r-d,0)
                nums+=1
    print(nums)
