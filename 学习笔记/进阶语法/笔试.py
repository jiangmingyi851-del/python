import heapq
prices=list(map(int,input().split()))
band=int(input())
def max_profit(prices, band):
        ans=0
        cur_win1=[]
        cur_win2=[]
        cur_min=prices[0]
        cur_max=prices[0]
        up=0
        down=0
        for i, j in enumerate(prices):
            up=i
            heapq.heappush(cur_win1,(j,i))
            heapq.heappush(cur_win2,(-j,i))
            if cur_min<=j<=cur_max:
                ans+=up-down+1
            elif j<cur_min:
                if cur_max-j>band:
                    while True:
                        if cur_win1[-1][0]>j+band or cur_win1[-1][1]< down:
                            a=heapq.heappop(cur_win1)
                            down=max(a[1]+1,down)
                        else:
                            break
                    cur_max=cur_win1[-1][0]
                    cur_min=j
                    ans+=up-down+1
            elif j>cur_max:
                if j-cur_min>band:
                    a=heapq.heappop(cur_win2)
                    down+=1
                    while True:
                        if -cur_win2[-1][0]<j-band or cur_win2[-1][1]< down:
                            a=heapq.heappop(cur_win1)
                            down=max(a[1]+1,down)
                        else:
                            break
                    cur_max=j
                    cur_min=-cur_win2[-1][0]
                    ans+=up-down+1

        return ans
print(max_profit(prices,band))
