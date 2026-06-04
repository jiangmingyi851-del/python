li=list(map(int,input().split()))
extra=int(input())
a=max(li)
for i in li:
    if i+extra>=a:
        print('1')
    else:
        print('0')