m=int(input())
for i in range(m):
    li=list(map(int,input().split()))
    lii=[i%24 for i in li]
    for i in range(1<<3):
        a=1
        s=[]
        num=lii[0]
        for j in range(1,4):
            if i%2==0:
                num+=li[j]
                s.append(1)
            else:
                num-=li[j]
                s.append(0)
            i//=2
        if num%24==0:
            num=li[0]
            for i,j in enumerate(s):
                if j==1:
                    num+=li[i+1]
                else:
                    num-=li[i+1]
            if num==24 or num==-24:
                print('Yes')
                a=0
                break
    if a==1:
        print('No')
    

        
        


        