import sys
def y(n,m):
    if n==0 or m==0:
        return
    if n==1:
        return 1
    return (y(n-1,m)+m-1)%n+1
while True:
    try:
        n,m=map(int,sys.stdin.readline().split())
        if m==0 and n==0:
            break
        print(y(n,m))
    except EOFError:
        break
