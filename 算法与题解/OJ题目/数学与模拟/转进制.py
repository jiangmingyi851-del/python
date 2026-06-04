def z(a):
    st=''
    while a>0:
        x=a%8
        st+=str(x)
        a=int((a-x)/8)
    st=st[::-1]
    return st
a=int(input())
print(z(a))