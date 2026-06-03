n=int(input())
value=list(map(int,input().split()))
i=len(bin(n)[2:])
value.extend([0]*(2**(i+3)-len(value)))
value.insert(0,0)
while i:
    for j in range(2**(i-1),2**i):
        value[j]=max(value[2*j]+value[2*j+1],value[j]+value[4*j]+value[4*j+1]+value[4*j+2]+value[4*j+3])
    i-=1
print(value[1])



