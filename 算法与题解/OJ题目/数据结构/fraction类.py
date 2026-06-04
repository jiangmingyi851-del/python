class Fraction():
    def __init__(self,a,b):
        self.a=a
        self.b=b
        assert self.b!=0
    def __add__(self,other):
        assert isinstance(other,Fraction)
        return Fraction(self.a*other.b+other.a*self.b,self.b*other.b)
    def __str__(self):
        for i in range(2,min(abs(self.a)//2,abs(self.b)//2)+1):
            while self.a%i==0 and self.b%i==0:
                self.a//=i
                self.b//=i
        if  self.b<0:
            self.a=-self.a
            self.b=-self.b
        return str(self.a)+"/"+str(self.b)
a,b,c,d=map(int,input().split())
f1=Fraction(a,b)
f2=Fraction(c,d)
print(f1+f2)


