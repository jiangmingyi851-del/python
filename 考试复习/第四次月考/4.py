n=int(input())
for i in range(n):
    li=list(map(int,input().split()))
    t=li[0]
    if t<=2:
        print('true')
    else:
        li=li[1:]
        dp=[[0]*t for i in range(t)] 
        for l in range(t):
            if t%2==1:
                dp[l][l]=li[l]
            else:
                dp[l][l]=-li[l]
        for length in range(2,t+1):
            for j in range(t-length+1):
                k=j+length-1
                if (t-length)%2==0:
                    dp[j][k]=max(dp[j+1][k]+li[j],dp[j][k-1]+li[k])
                else:
                    dp[j][k]=min(dp[j+1][k]-li[j],dp[j][k-1]-li[k])
        if dp[0][t-1]>=0:
            print('true')
        else:
            print('false')
                
