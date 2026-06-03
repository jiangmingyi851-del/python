def max_two(prices):
    n=len(prices)
    if n < 2:
        return "Error: At least two prices are required"
    left_profits=[0]*n
    right_profits=[0]*n
    min_price=prices[0]
    for i in range(1,n):
        min_price=min(min_price,prices[i])
        left_profits[i]=max(left_profits[i-1],prices[i]-min_price)
    max_price=prices[-1]
    for i in range(n-2,-1,-1):
        max_price=max(max_price,prices[i])
        right_profits[i]=max(right_profits[i+1],max_price-prices[i])
    max_total_profit=0
    for i in range(n):
        max_total_profit=max(max_total_profit,left_profits[i]+right_profits[i])
    return max_total_profit
lis=[]
t=int(input().strip())
for _ in range(t):
    n= int(input().strip())
    a=list(map(int,input().strip().split()))
    if len(a)!=n:
        continue
    lis.append(a)
for a in lis:
    print(max_two(a))

import sys

def max_two_profit(prices):
    buy1 = float('-inf')
    sell1 = 0
    buy2 = float('-inf')
    sell2 = 0
    
    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)
    
    return sell2

def main():
    t = int(sys.stdin.readline().strip())
    for _ in range(t):
        n = int(sys.stdin.readline().strip())
        line = sys.stdin.readline().strip()
        if not line:
            continue
        prices = list(map(int, line.split()))
        print(max_two_profit(prices))

if __name__ == "__main__":
    main()
