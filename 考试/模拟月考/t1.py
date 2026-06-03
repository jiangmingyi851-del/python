def pr(s,l):
    if s==1 and l==1:
        a=' /\\'
        b='/__\\'
        return [a,b]
    else:
        if l==1:
            l1=pr(s-1,1)
            l2=pr(s-1,2)
            for i,j in enumerate(l1):
                l1[i]=' '*2**(s-1)+j
            l1.extend(l2)
            return l1
        if l==2:
            l1=pr(s,1)
            r=len(l1)
            for i,j in enumerate(l1):
                l1[i]=l1[i]+' '*(r-1-i)+l1[i]
            return l1
while True:
    s=int(input())
    if s==0:
        break
    l=pr(s,1)
    for i in l:
        print(i)
    print()


        
