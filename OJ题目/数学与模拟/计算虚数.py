import cmath
import math
def Unary_quadratic_equation(a,b,c):
    x1=(-b+cmath.sqrt(b*b-4*a*c))/(2*a)
    x2=(-b-cmath.sqrt(b*b-4*a*c))/(2*a)
    if x1.real<x2.real:
        x1,x2=x2,x1
    if  x1.imag<x2.imag:
        x1,x2=x2,x1
    return x1,x2
n=int(input())
li=[]
for _ in range(n):
    a,b,c=map(float,input().split())
    x1,x2=Unary_quadratic_equation(a,b,c)
    li.append((x1,x2))
for i in li:
    x1,x2=i
    x1_real=x1.real
    x2_real=x2.real
    if abs(x1.real)<1e-10:
        x1_real=0.0
    if abs(x2.real)<1e-10:
        x2_real=0.0
    
    if abs(x1.imag)<1e-10:
        if abs(x1.real-x2.real)<1e-10:
            print(f"x1=x2={x1_real:.5f}")
        else:
            print(f"x1={x1_real:.5f};x2={x2_real:.5f}")
    else:
        print(f"x1={x1_real:.5f}+{x1.imag:.5f}i;x2={x2_real:.5f}-{x1.imag:.5f}i")