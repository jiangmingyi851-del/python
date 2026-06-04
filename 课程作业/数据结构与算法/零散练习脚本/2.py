s=input()
n=len(s)
num=0
for i,j in enumerate(s):
    if j=='I':
        if i!=n-1 and (s[i+1]=='V' or s[i+1]=='X'):
                num-=1
        else:
            num+=1
    if j=='V':
        num+=5
    if j=='X':
        if i!=n-1 and(s[i+1]=='L' or s[i+1]=='C'):
            num-=10
        else:
            num+=10
    if j=='L':
        num+=50
    if j=='C':
        if i!=n-1 and (s[i+1]=='D' or s[i+1]=='M'):
            num-=100
        else:
            num+=100
    if j=='D':
        num+=500
    if j=='M':
        num+=1000
print(num)

